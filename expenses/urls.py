from .views import ExpenseViewSet, CategoryViewSet, InstallmentExpenseViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='expense-category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'installments', InstallmentExpenseViewSet, basename='installment-expense')

urlpatterns = [
    path('', include(router.urls))
]
