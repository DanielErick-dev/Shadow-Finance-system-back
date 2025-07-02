from django.contrib import admin
from expenses.models import Expense, TypeOfExpense


@admin.register(TypeOfExpense)
class TypeOfExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "type_of_expense":
            kwargs["queryset"] = TypeOfExpense.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_of_expense', 'total_value', 'payment_status', 'user', )
    list_filter = ('payment_status', 'type_of_expense', 'user', )
    search_fields = ('name', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "type_of_expense":
            kwargs["queryset"] = TypeOfExpense.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
