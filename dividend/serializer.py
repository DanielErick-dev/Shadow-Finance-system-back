from .models import Ativo, ItemDividendo, CardDividendoMes
from rest_framework import serializers


class AtivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ativo
        fields = ['id', 'codigo', 'tipo']


class ItemDividendoSerializer(serializers.ModelSerializer):
    ativo = AtivoSerializer(read_only=True)
    ativo_id = serializers.PrimaryKeyRelatedField(
        queryset=Ativo.objects.all(), source='ativo', write_only=True
    )
    data = serializers.DateField(source='data_recebimento')

    class Meta:
        model = ItemDividendo
        fields = ['id', 'ativo', 'ativo_id', 'valor', 'data', 'card_mes']
        extra_kwargs = {
            'card_mes': {'write_only': True}
        }


class CardDividendoMesSerializer(serializers.ModelSerializer):
    itens = ItemDividendoSerializer(many=True, read_only=True)

    class Meta:
        model = CardDividendoMes
        fields = ['id', 'mes', 'ano', 'itens']
