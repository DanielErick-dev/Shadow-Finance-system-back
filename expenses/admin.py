from django.contrib import admin
from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', )
    search_fields = ('name', 'user__username', )
    ordering = ('name', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount', 'due_date', 'category', 'paid', 'user', )
    search_fields = ('name', 'category__name', 'user__username', )
    list_filter = ('paid', 'due_date', 'category', 'user')
    ordering = ('-due_date', )
    list_editable = ('paid', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field == 'category':
            kwargs["queryset"] = Category.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
