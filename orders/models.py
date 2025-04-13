from django.db import models
from users.models import User 
from payments.models import PaymentModel as Payment
import uuid


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
    order_status = models.CharField(choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0], max_length=2)
    order_date = models.DateTimeField(auto_now=True)
    order_update_date = models.DateTimeField(auto_now_add=True)
    
    # Shipping information
    address = models.CharField(max_length=400, null=False, blank=False)
    postal_code = models.CharField(max_length=256, null=False, blank=False)
    # Payment info
    payment_status = models.ForeignKey(Payment, on_delete=models.CASCADE)
