import uuid
from django.db import models
from orders_app.models import Order
from users_app.models import User


class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    upi_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    upi_reference_no = models.CharField(max_length=100, blank=True, null=True)
    upi_payer_vpa = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.payment_status} - ₹{self.amount}"

# Create your models here.
