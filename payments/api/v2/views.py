from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings

from orders.models import Order
from ...models import PaymentModel
from .throttles import PaymentRequestThrottle

import requests


class PaymentOrderRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    throttle_classes = [PaymentRequestThrottle,]
        
    def post(self, request, uuid):
        order = Order.objects.get(order_id=uuid)
        user = request.user
        
        if not order or order.user != user:
            return Response({"msg": "Invalid payment data",}, status=status.HTTP_400_BAD_REQUEST)
        
        total_price = order.total_price
        payment = order.order_payment  # Use the payment model related name which is defined in order model.
        if payment.status == "S":
            return Response({"msg": "the order is already payed"}, status=status.HTTP_200_OK)
        callback_url = request.build_absolute_uri(reverse('payments:api-v2:payment-verify'))
        data = {
            "MerchantID": settings.MERCHANT_ID,
            "Amount": total_price,
            "Description": 'description',
            "CallbackURL": callback_url
        }
        response = requests.post(url=settings.ZARINPAL_REQUEST_URL, data=data)
        result = response.json()
        
        if result.get("Status") == 100:
            authority = result["Authority"]
            payment.authority = authority
            payment.save()
            # Not that, dont set the payment status as successed here, we will handle that in out verification view.    
            payment_url = settings.ZARINPAL_STARTPAY_URL.format(authority=authority)
            return Response({
                "payment_url": payment_url,
                "authority": authority
            }, status=status.HTTP_200_OK)
        else:
            payment.status = "F"  # Failed
            payment.save()
            return Response(data={
                'status': result.get("Status"),
                "message": "Payment request failed",
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderPaymentVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        authority = request.GET.get("Authority")
        status_param = request.GET.get("Status") 
        if not authority or not status_param:
            return Response({"error": "Missing authority or status"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = PaymentModel.objects.get(authority=authority, user=request.user)
        except PaymentModel.DoesNotExist:
            return Response(data={"Error": "Payment model does not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if status_param != "OK":
            payment.status = "F"
            payment.save()
            return Response({"message": "Payment was cancelled or failed"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "MerchantID": settings.MERCHANT_ID,
            "Amount": payment.amount,
            "Authority": authority
        }

        response = requests.post(settings.ZARINPAL_VERIFY_URL, data=data)
        result = response.json()

        if result.get("Status") == 100:            
            payment.status = "S"  # Successful
            payment.ref_id = result.get("RefID")
            payment.save()
            
            return Response(data={
                "message": "Payment succussful",
                'ref_id': result.get("RefID"),
            }, status=status.HTTP_200_OK)
            
        else:
            payment.status = "F"  # Failed
            payment.save()
            
            return Response({
                "message": "Payment verification failed",
                "status": result.get("Status")
            }, status=status.HTTP_400_BAD_REQUEST)