from django.db import models
from expenses.models import Expense


class Installment(models.Model):
    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name='installments',
        verbose_name='Despesa'
    )
    installment_number = models.PositiveIntegerField(
        verbose_name='Número da Parcela'
    )
    installment_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor da Parcela'
    )
    due_date = models.DateField(verbose_name='Data de Vencimento')
    is_paid = models.BooleanField(
        default=False,
        verbose_name='Pago'
    )

    class Meta:
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['due_date']
        unique_together = ['expense', 'installment_number']

    def __str__(self):
        return f"Parcela {self.number} - {self.expense.name}"
