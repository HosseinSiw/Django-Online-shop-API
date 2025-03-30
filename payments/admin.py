from django.contrib import admin
from .models import PaymentModel


class PaymentAdmin(admin.ModelAdmin):
    list_filter = ['status', 'user', 'amount']
    list_display = ['user', "amount", "status",]
    search_fields = ['user', 'status', 'authority', 'ref_id']
    ordering = 'user'
    
    
