from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import Expense, Category
from .serializer import ExpenseSerializer, CategorySerializer
from .mixins import UserQuerysetMixin
from .filters import ExpenseFilter
import django_filters


class CategoryViewSet(UserQuerysetMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(UserQuerysetMixin, viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpenseFilter
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['name']
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
