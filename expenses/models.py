from django.db import models
from costumers.models import CustomUser


class TypeOfExpense(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Nome do Tipo de Despesa'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='expense_types',
        null=True,
        blank=True,
        verbose_name='Usuário'
    )

    class Meta:
        verbose_name = 'Tipo de Despesa'
        verbose_name_plural = 'Tipos de Despesas'
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_STATUS = [
        ('paid', 'pago'),
        ('pending', 'pendente'),
    ]
    name = models.CharField(
        max_length=100,
        verbose_name='Nome da Despesa'
    )
    type_of_expense = models.ForeignKey(
        TypeOfExpense,
        on_delete=models.CASCADE,
        verbose_name='Tipo de Despesa'
    )
    total_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor Total'
    )
    payment_status = models.CharField(
        max_length=7,
        choices=PAYMENT_STATUS,
        default='pending',
        verbose_name='Status de Pagamento'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='expenses'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    is_installment = models.BooleanField(
        default=False,
        verbose_name='Parcelado',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_payment_status_display()})"
