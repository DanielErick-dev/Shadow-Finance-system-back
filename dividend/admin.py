from django.contrib import admin
from .models import Ativo, CardDividendoMes, ItemDividendo


class AtivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'user', 'tipo')
    search_fields = ('codigo', 'tipo')
    list_filter = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ativo":
            kwargs["queryset"] = Ativo.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CardDividendoMesAdmin(admin.ModelAdmin):
    list_display = ('user', 'mes', 'ano', 'created_at', 'updated_at')
    search_fields = ('user__username', 'mes', 'ano')
    list_filter = ('user',)
    ordering = ('-ano', '-mes')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = CardDividendoMes.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ItemDividendoAdmin(admin.ModelAdmin):
    list_display = ('card_mes', 'ativo', 'valor', 'created_at', 'data_recebimento')
    search_fields = ('card_mes__user__username', 'ativo__codigo', 'valor')
    list_filter = ('card_mes__user',)
    ordering = ('-created_at',)


admin.site.register(Ativo, AtivoAdmin)
admin.site.register(CardDividendoMes, CardDividendoMesAdmin)
admin.site.register(ItemDividendo, ItemDividendoAdmin)
