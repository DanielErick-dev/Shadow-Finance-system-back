import django_filters
from .models import CardDividendoMes


class CardDividendoMesFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(field_name='ano', lookup_expr='exact')
    mes = django_filters.NumberFilter(field_name='mes', lookup_expr='exact')

    class Meta:
        model = CardDividendoMes
        fields = ['ano', 'mes']
