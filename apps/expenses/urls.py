from django.urls import path
from .views import ExpenseCategoryViewSet, PaymentViewSet, PaymentSummaryViewSet


app_name = 'apps.expenses'

urlpatterns = [
    path('categories', ExpenseCategoryViewSet.as_view({'get': 'list','post': 'create'}), name='expenseview'),
    path('categories/<int:pk>', ExpenseCategoryViewSet.as_view({'get': 'retrieve','put': 'update',
                'patch': 'update','delete': 'destroy'}), name='expensedetailview'),
    
    path('<str:state>', PaymentViewSet.as_view({'get': 'list','post': 'create'}), name='paymentview'),
    path('<str:state>/<int:pk>', PaymentViewSet.as_view({'get': 'retrieve','put': 'update',
                'patch': 'update','delete': 'destroy'}), name='paymentdetailview'),
    
    path('<int:pk>/summary', PaymentSummaryViewSet.as_view({'get': 'list','post': 'create'}), name='paymentsummaryview'),
    path('<int:pk>/summary/<int:num>', PaymentSummaryViewSet.as_view({'get': 'retrieve','put': 'update',
                'patch': 'update','delete': 'destroy'}), name='paymentsummarydetailview')
]
