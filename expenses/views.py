from .models import Expense, TypeOfExpense
from rest_framework import generics
from .serializer import TypeOfExpenseSerializer, ExpenseSerializer
from rest_framework.permissions import IsAuthenticated


class TypeOfExpenseListApiView(generics.ListCreateAPIView):
    queryset = TypeOfExpense.objects.all()
    serializer_class = TypeOfExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TypeOfExpense.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseListCreateApiView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
