from django.db import models
from costumers.models import CustomUser


class TipoAtivo(models.TextChoices):
    ACAO = 'ACAO', 'Ação'
    FII = 'FII', 'Fundo Imobiliário'
    BDR = 'BDR', 'BDR'
    ETF = 'ETF', 'ETF'


class Ativo(models.Model):
    codigo = models.CharField(max_length=10)
    tipo = models.CharField(max_length=4, choices=TipoAtivo.choices, default=TipoAtivo.ACAO)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('codigo', 'user')
        ordering = ['codigo']

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo


class CardDividendoMes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mes = models.IntegerField()
    ano = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Card de Dividendo do Mês"
        verbose_name_plural = 'Cards de Dividendos do mês'
        unique_together = ('user', 'mes', 'ano')
        ordering = ['-ano', '-mes']


class ItemDividendo(models.Model):
    card_mes = models.ForeignKey(CardDividendoMes, on_delete=models.CASCADE, related_name='itens')
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_recebimento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
