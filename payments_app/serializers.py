from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_token = serializers.CharField(source='order.token_number', read_only=True)
    order_status = serializers.CharField(source='order.order_status', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'amount', 'payment_method',
            'upi_transaction_id', 'upi_reference_no', 'upi_payer_vpa',
            'payment_status', 'paid_at', 'created_at',
            'order_token', 'order_status'
        ]
        read_only_fields = ['payment_status', 'paid_at', 'created_at']