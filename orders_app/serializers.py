from rest_framework import serializers
from .models import Order, OrderItem
from products_app.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['product_name', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_name = serializers.CharField(source='user.full_name', read_only=True)
    customer_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_status', 'total_amount', 'payment_method',
            'payment_status', 'token_number', 'delivery_address',
            'notes', 'placed_at', 'approved_at',
            'customer_name', 'customer_phone', 'items'
        ]
        read_only_fields = ['order_status', 'payment_status', 'token_number', 'placed_at', 'approved_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            unit_price = product.price
            subtotal = unit_price * quantity
            total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )

        order.total_amount = total
        order.save()
        return order