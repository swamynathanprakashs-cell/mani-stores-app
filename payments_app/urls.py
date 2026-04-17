from django.urls import path
from .views import RecordPaymentView, TransactionHistoryView, PaymentDetailView

urlpatterns = [
    path('pay/', RecordPaymentView.as_view(), name='record-payment'),
    path('history/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('<uuid:order_id>/', PaymentDetailView.as_view(), name='payment-detail'),
]