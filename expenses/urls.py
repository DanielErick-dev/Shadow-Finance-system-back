from django.urls import path
from .views import ExpenseListCreateApiView, TypeOfExpenseListApiView


urlpatterns = [
    path(
        'expenses/',
        ExpenseListCreateApiView.as_view(),
        name='expense_list_create'
    ),
    path(
        'type_of_expenses/',
        TypeOfExpenseListApiView.as_view(),
        name='type_of_expense_list_api_view'
    ),
]
