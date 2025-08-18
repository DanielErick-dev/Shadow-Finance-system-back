import datetime
from expenses.models import Expense, RecurringExpense, PaidRecurringExpense
from expenses.serializer import ExpenseSerializer, CategorySerializer


class MonthlyExpenseLogic:
    def __init__(self, user, year: int, month: int):
        self.user = user
        self.year = year
        self.month = month

    def get_monthly_expenses(self) -> list:
        real_expenses = self._get_real_expenses()
        virtual_expenses = self._get_virtual_recurring_expenses()
        real_expenses_data = ExpenseSerializer(real_expenses, many=True).data

        for expense_data in real_expenses_data:
            expense_data['is_recurring'] = False

        combined_list = sorted(
            real_expenses_data + virtual_expenses,
            key=lambda x: x['due_date']
        )
        return combined_list

    def _get_real_expenses(self):
        return Expense.objects.filter(
            user=self.user,
            due_date__year=self.year,
            due_date__month=self.month
        )

    def _get_virtual_recurring_expenses(self) -> list:
        active_contracts = RecurringExpense.objects.filter(
            user=self.user,
            active=True,
            start_date__lte=datetime.date(self.year, self.month, 28)
        )

        paid_recurring_ids = PaidRecurringExpense.objects.filter(
            recurring_expense__user=self.user,
            year=self.year,
            month=self.month
        ).values_list('recurring_expense_id', flat=True)

        virtual_expenses = []
        for contract in active_contracts:
            if contract.end_date and contract.end_date < datetime.date(self.year, self.month, 1):
                continue
            virtual_expense = {
                'id': f'rec-{contract.id}',
                'name': contract.name,
                'amount': contract.amount,
                'due_date': datetime.date(self.year, self.month, contract.due_day),
                'category': CategorySerializer(
                    contract.category).data if contract.category else None,
                'paid': contract.id in paid_recurring_ids,
                'is_recurring': True,
                'payment_date': None,
                'installment_origin': None,
                'created_at': contract.created_at
            }
            virtual_expenses.append(virtual_expense)
        return virtual_expenses
