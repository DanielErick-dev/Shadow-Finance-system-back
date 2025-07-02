from django.contrib import admin
from installments.models import Installment


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('expense', 'installment_number', 'installment_value', 'due_date', 'is_paid', )
    list_filter = ('is_paid', 'expense__user', )
    search_fields = ('expense__name',)
