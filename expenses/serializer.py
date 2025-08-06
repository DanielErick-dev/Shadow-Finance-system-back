from rest_framework import serializers
from .models import Expense, Category, InstallmentExpense


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class InstallmentExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = InstallmentExpense
        fields = [
            'id',
            'name',
            'total_amount',
            'installments_quantity',
            'first_due_date',
            'category',
            'category_id'
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        allow_null=True,
        required=False
    )
    installment_origin = InstallmentExpenseSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Expense
        fields = [
            'id',
            'name',
            'amount',
            'due_date',
            'payment_date',
            'category',
            'category_id',
            'installment_origin',
            'paid',
            'created_at'
        ]
