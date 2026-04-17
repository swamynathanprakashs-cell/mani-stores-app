from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import date
from .models import Order, OrderItem
from .serializers import OrderSerializer


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                'message': 'Order placed successfully',
                'order': OrderSerializer(order, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-placed_at')
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


class ApproveOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk)

            # Generate token (cycles 1-30)
            today = date.today()
            last_token = Order.objects.filter(
                placed_at__date=today,
                token_number__isnull=False
            ).order_by('-placed_at').first()

            if last_token and last_token.token_number:
                last_seq = int(last_token.token_number.split('-')[-1])
                next_seq = 1 if last_seq >= 30 else last_seq + 1
            else:
                next_seq = 1

            token = f"TKN-{today.strftime('%Y%m%d')}-{str(next_seq).zfill(2)}"

            order.token_number = token
            order.order_status = 'approved'
            order.approved_at = timezone.now()
            order.approved_by = request.user
            order.save()

            return Response({
                'message': 'Order approved',
                'token_number': token,
                'order_id': str(order.id)
            })
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# Create your views here.
