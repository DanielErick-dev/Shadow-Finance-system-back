from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import Expense, Category, InstallmentExpense, PaidRecurringExpense, RecurringExpense
from .serializer import (
    ExpenseSerializer,
    CategorySerializer,
    InstallmentExpenseSerializer,
    PaidRecurringExpenseSerializer,
    RecurringExpenseSerializer
)
from expenses.services.installment_manager_service import InstallmentExpenseService
from .mixins import UserQuerysetMixin
from .filters import ExpenseFilter
import django_filters
from datetime import datetime


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


class RecurringExpenseViewSet(UserQuerysetMixin, viewsets.ModelViewSet):
    queryset = RecurringExpense.objects.all()
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaidRecurringExpenseViewSet(UserQuerysetMixin, viewsets.ModelViewSet):
    queryset = PaidRecurringExpense.objects.select_related('recurring_expense').all()
    serializer_class = PaidRecurringExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(recurring_expense__user=self.request.user)

    def perform_create(self, serializer):
        recurring_expense = serializer.validated_data.get('recurring_expense')
        if recurring_expense.user != self.request.user:
            raise serializers.ValidationError('você não tem permissão para pagar esta despesa')
        serializer.save()


class MonthlyExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            year = int(request.query_params.get('year', datetime.date.today().year))
            month = int(request.query_params.get('month', datetime.date.today().month))
        except (TypeError, ValueError):
            return Response({
                'error': 'parãmetros de ano/mês inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        real_expenses = Expense.objects.filter(
            user=request.user,
            due_date__year=year,
            due_date__month=month
        )

        recurring_contracts = RecurringExpense.objects.filter(
            user=request.user,
            active=True,
            start_date__lte=datetime.date(year, month, 28)
        )

        paid_recurring_ids = PaidRecurringExpense.objects.filter(
            recurring_expense__user=request.user,
            year=year,
            month=month
        ).values_list('recurring_expense_id', float=True)

        virtual_expenses = []
        for contract in recurring_contracts:
            if contract.end_date and contract.end_date < datetime.date(year, month, 1):
                continue
    
            virtual_expense = {
                'id': f'rec-{contract.id}',
                'name': contract.name,
                'amount': contract.amount,
                'due_date': datetime.date(year, month, contract.due_day),
                'category': CategorySerializer(
                    contract.category).data if contract.category else None,
                'paid': contract.id in paid_recurring_ids,
                'is_recurring': True
            }
            virtual_expenses.append(virtual_expense)
        real_expenses_data = ExpenseSerializer(real_expenses, many=True).data

        for expense_data in real_expenses_data:
            expense_data['is_recurring'] = False
 
        combined_list = sorted(
            real_expenses_data + virtual_expenses,
            key=lambda x: x['due_date']
        )

        return Response(combined_list)
