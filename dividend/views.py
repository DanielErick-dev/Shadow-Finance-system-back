from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Ativo, CardDividendoMes, ItemDividendo
from .filters import CardDividendoMesFilter
from . serializer import (
    AtivoSerializer,
    ItemDividendoSerializer,
    CardDividendoMesSerializer
)


class AtivoViewSet(viewsets.ModelViewSet):
    serializer_class = AtivoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Ativo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CardDividendoMesViewSet(viewsets.ModelViewSet):
    serializer_class = CardDividendoMesSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CardDividendoMesFilter

    def get_queryset(self):
        return CardDividendoMes.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemDividendoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemDividendoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ItemDividendo.objects.filter(card_mes__user=self.request.user)

    def perform_create(self, serializer):
        card_mes_id = self.request.data.get('card_mes')
        if not card_mes_id:
            raise serializers.ValidationError(
                {'card_mes': 'este campo é obrigatório'}
            )
        try:
            card_pai = CardDividendoMes.objects.get(
                id=card_mes_id, user=self.request.user
            )
        except CardDividendoMes.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'card de Mês inválido ou não pertence a voce'}
            )
        serializer.save(card_mes=card_pai)
