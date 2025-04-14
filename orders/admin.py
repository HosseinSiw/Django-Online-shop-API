from django.contrib import admin
from .models import Order
 

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'full_name', 'total_price', "order_status"]
    list_filter = ['user', 'full_name', 'order_status', "payment_status"]
    search_fields = ['order_id', 'phone_number', 'full_name',]
    ordering = ('-order_date',)
    

admin.site.register(Order, OrderAdmin)