from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AtivoViewSet,
    CardDividendoMesViewSet,
    ItemDividendoViewSet
)


router = DefaultRouter()

router.register(r'cards-dividendos', CardDividendoMesViewSet, basename='card-dividendo')
router.register(r'ativos', AtivoViewSet, basename='ativo')

item_dividendo_list = ItemDividendoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

item_dividendo_detail = ItemDividendoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path('itens-dividendos/', item_dividendo_list, name='item-dividendo-list'),
    path('itens-dividendos/<int:pk>/', item_dividendo_detail, name='item-dividendo-detail')
]
