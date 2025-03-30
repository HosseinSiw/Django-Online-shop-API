from django.db import models
from users.models import User


class PaymentModel(models.Model):
    payment_status_choices = [
        ("P", "Pending"),
        ('S', 'Success'),
        ("F", "Failure"),
    ]
    status = models.CharField(choices=payment_status_choices, max_length=10, default='P')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    authority = models.CharField(max_length=255, blank=True, null=True)
    ref_id = models.CharField(max_length=255, blank=True, null=True)   
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        msg = f'{self.user.email} - {self.amount} - {self.id}'
        return msg