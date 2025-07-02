from rest_framework import serializers
from .models import TypeOfExpense, Expense


class TypeOfExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfExpense
        fields = ['name']


class ExpenseSerializer(serializers.ModelSerializer):
    type_of_expense = serializers.PrimaryKeyRelatedField(
        queryset=TypeOfExpense.objects.all()
    )

    class Meta:
        model = Expense
        fields = '__all__'
