from django.db import models
from users.models import User 
from payments.models import PaymentModel as Payment

from products.models import Product 

import uuid
from decimal import Decimal


ORDER_STATUSES = [
    ("P", "Pending"),
    ("Pr", "Processing"),
    ('S', "Shipped"),
    ("D", "Delivered"),
    ("C", "Cancelled"),
]

class Order(models.Model):
    """
    Main Order Model Class.
    """
    # Basic information of a single order recorde.
    order_id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    full_name = models.CharField(max_length=20, null=False, blank=False)
    
    order_status = models.CharField(choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0], max_length=2)
    order_date = models.DateTimeField(auto_now=True)
    order_update_date = models.DateTimeField(auto_now_add=True)
    
    
    # Shipping information
    address = models.CharField(max_length=400, null=False, blank=False)
    postal_code = models.CharField(max_length=256, null=False, blank=False)
    # Payment info
    total_price = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        default=Decimal('0.01'), 
    )
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, )
    payment_status = models.CharField(max_length=1, choices=Payment.payment_status_choices, default='P')
    
    def __str__(self):
        msg = f'Order: {self.order_id} - Date: {self.order_date} - User: {self.user} - status: {self.order_status}'
        return msg

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
