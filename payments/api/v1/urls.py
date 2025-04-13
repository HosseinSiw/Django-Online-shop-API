from django.urls import path
from .views import PaymentRequestView, PaymentVerifyView


app_name = 'api-v1'
urlpatterns = [
    path("request/", PaymentRequestView.as_view(), name='payment-request'),
    path("verify/", PaymentVerifyView.as_view(), name='payment-verify'),
]