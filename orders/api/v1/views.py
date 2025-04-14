from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from payments.models import PaymentModel as Payment
from cart.models import Cart
from ...models import Order, OrderItem    
from .serializers import OrderSerializer


class OrderCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    
    def post(self, request):
        user = request.user
        user_cart = Cart.objects.get(user=user)
        
        
        if user_cart.item_counts == 0:
            return Response(
                {"msg": "your cart is clear, please choose some items and try again."},
                status=status.HTTP_204_NO_CONTENT,
            )
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                valid_data = serializer.validated_data
                payment = Payment.objects.create(user=request.user, 
                                                 amount=user_cart.cart_total_price,)
                order = Order.objects.create(
                    user=user,
                    total_price=user_cart.cart_total_price,
                    address=valid_data['address'],
                    postal_code=valid_data['postal_code'],
                    phone_number=valid_data['phone_number'],
                    full_name=valid_data['full_name'],
                    payment=payment,
                )
                for item in user_cart.cart_items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )
                    
                user_cart.clear_cart()
                
            data = {
                "message": "Order Placed successfully",
                "order_id": order.order_id,
                "total_price": order.total_price,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
