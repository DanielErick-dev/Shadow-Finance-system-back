from rest_framework import serializers
from .models import Expense, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        allow_null=True,
        required=False

    )

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
            'paid',
            'created_at'
        ]
