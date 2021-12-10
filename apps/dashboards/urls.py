from .views import ProjectsIncomeDashView, ExpenseDashView, CashFlowDashView
from django.urls import path

urlpatterns = [
    path('project-income/', ProjectsIncomeDashView.as_view(), name='projectincomeview'),
    # All Service Income View
    # Single Service Income View
    path('expense-dash/', ExpenseDashView.as_view(), name='expensedashview'),
    path('cashflow/', CashFlowDashView.as_view(), name='cashflowview')
]
