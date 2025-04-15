from django.urls import path
from . import views as V

app_name = 'api-v2'

urlpatterns = [
    path("order_payment_request/<uuid:uuid>/", V.PaymentOrderRequestView.as_view(), 
    name='order_payment_reuqest'),
    path('order_payment_verify/', V.OrderPaymentVerifyView.as_view(), name='order_payment_verify')
]