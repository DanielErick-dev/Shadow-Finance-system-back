from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import Expense, Category, InstallmentExpense
from .serializer import ExpenseSerializer, CategorySerializer, InstallmentExpenseSerializer
from expenses.services.installment_manager_service import InstallmentExpenseService
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


class InstallmentExpenseViewSet(UserQuerysetMixin, viewsets.ModelViewSet):
    queryset = InstallmentExpense.objects.all()
    serializer_class = InstallmentExpenseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        service = InstallmentExpenseService(
            user=request.user,
            name=validated_data.get('name'),
            total_amount=validated_data.get('total_amount'),
            installments_quantity=validated_data.get('installments_quantity'),
            first_due_date=validated_data.get('first_due_date'),
            category=validated_data.get('category')
        )
        installment_expense = service.create()
        response_serializer = self.get_serializer(installment_expense)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
