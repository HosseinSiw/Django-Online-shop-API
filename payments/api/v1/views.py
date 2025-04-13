import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from django.conf import settings
from cart.models import Cart
from ...models import PaymentModel


class PaymentRequestView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        user = request.user
        amount = Cart.objects.get(user=user).cart_total_price  # Fetch the users cart price. 
        
        if amount <= 0:
            return Response(data={"error": "The cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        payment = PaymentModel.objects.create(
            user=request.user,
            amount=amount,
            status="P"
        )
        callback_url = request.build_absolute_uri(reverse('payments:api-v1:payment-verify'))
        data = {
            "MerchantID": settings.MERCHANT_ID,
            "Amount": amount,
            "Description": 'description',
            "CallbackURL": callback_url
        }
        response = requests.post(url=settings.ZARINPAL_REQUEST_URL, data=data)
        result = response.json()
        
        if result.get("Status") == 100:
            authority = result["Authority"]
            payment.authority = authority
            payment.save()
            
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


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

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