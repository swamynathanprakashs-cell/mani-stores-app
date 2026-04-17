from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Payment
from orders_app.models import Order
from .serializers import PaymentSerializer


class RecordPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if payment already exists
        if Payment.objects.filter(order=order).exists():
            return Response({'error': 'Payment already recorded for this order'},
                            status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_amount,
            payment_method=request.data.get('payment_method'),
            upi_transaction_id=request.data.get('upi_transaction_id', ''),
            upi_reference_no=request.data.get('upi_reference_no', ''),
            upi_payer_vpa=request.data.get('upi_payer_vpa', ''),
            payment_status='completed',
            paid_at=timezone.now()
        )

        # Update order payment status
        order.payment_status = 'paid'
        order.save()

        return Response({
            'message': 'Payment recorded successfully',
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(
            user=request.user
        ).order_by('-created_at').select_related('order')

        history = []
        for payment in payments:
            order = payment.order
            items = order.items.all()
            history.append({
                'order_id': str(order.id),
                'token_number': order.token_number,
                'order_date': order.placed_at,
                'order_status': order.order_status,
                'payment_method': payment.payment_method,
                'payment_status': payment.payment_status,
                'total_amount': str(order.total_amount),
                'upi_transaction_id': payment.upi_transaction_id,
                'paid_at': payment.paid_at,
                'items': [
                    {
                        'product_name': item.product_name,
                        'quantity': item.quantity,
                        'unit_price': str(item.unit_price),
                        'subtotal': str(item.subtotal)
                    } for item in items
                ]
            })

        return Response(history)


class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            payment = Payment.objects.get(order__id=order_id, user=request.user)
            order = payment.order
            items = order.items.all()

            return Response({
                'order_id': str(order.id),
                'token_number': order.token_number,
                'order_status': order.order_status,
                'payment_method': payment.payment_method,
                'payment_status': payment.payment_status,
                'total_amount': str(order.total_amount),
                'upi_transaction_id': payment.upi_transaction_id,
                'paid_at': payment.paid_at,
                'delivery_address': order.delivery_address,
                'items': [
                    {
                        'product_name': item.product_name,
                        'quantity': item.quantity,
                        'unit_price': str(item.unit_price),
                        'subtotal': str(item.subtotal)
                    } for item in items
                ]
            })
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)