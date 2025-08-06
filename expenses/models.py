from django.db import models
from costumers.models import CustomUser


class Category(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='expense_categories',
        verbose_name='Usuário'
    )
    name = models.CharField(max_length=100, verbose_name='Nome')

    class Meta:
        verbose_name = 'Categoria De Despesa'
        verbose_name_plural = 'Categorias De Despesas'
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class InstallmentExpense(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='installment_expenses',
        verbose_name='Usuário'
    )
    name = models.CharField(max_length=255, verbose_name='Nome da Compra')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor Total')
    installments_quantity = models.PositiveIntegerField(verbose_name='Quantidade de Parcelas')
    first_due_date = models.DateField(verbose_name='Data Da Primeira Parcela')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='categoria',
        related_name='installment_expenses',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Despesa Parcelada'
        verbose_name_plural = 'Despesas Parceladas'
        ordering = ['-first_due_date']

    def __str__(self):
        return f'{self.name} ({self.installments_quantity}x)'


class Expense(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Usuário'
    )
    name = models.CharField(max_length=255, verbose_name='Nome da Despesa')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    due_date = models.DateField(verbose_name='Data de Vencimento')
    payment_date = models.DateField(
        verbose_name='Data de Pagamento',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='categoria',
        related_name='expenses',
        null=True,
        blank=True
    )
    paid = models.BooleanField(default=False, verbose_name='Pago')
    installment_origin = models.ForeignKey(
        InstallmentExpense,
        on_delete=models.CASCADE,
        verbose_name='parcelado',
        related_name='installments',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'despesas'
        ordering = ['due_date']

    def __str__(self):
        return self.name
