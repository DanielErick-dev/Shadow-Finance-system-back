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


class Expense(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Usuário'
    )
    name = models.CharField(max_length=255, verbose_name='Nome da Despesa')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    due_date = models.DateField(verbose_name='Data de Vencimento / Referência')
    payment_date = models.DateField(
        verbose_name='Data de Pagamento',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='expenses',
        null=True,
        blank=True
    )
    paid = models.BooleanField(default=False, verbose_name='Pago')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'despesas'
        ordering = ['due_date']

    def __str__(self):
        return self.name
