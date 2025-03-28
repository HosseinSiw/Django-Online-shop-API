from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from cart.models import Cart, CartItem
from users.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import AddToCartSerializer


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AddToCartSerializer
    
    def post(self, request, product_id: int, *args, **kwargs):
        quantity = int(request.data.get("quantity", 1))
        
        data = {
            "quantity": quantity,
            "product_id": product_id,
        }
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            product = get_object_or_404(Product, pk=product_id)
            
            print("\n\n\nREQUEST BY:", request.user)
            print("\nEMAIL ADDRESS:", request.user.email)
            print(type(request.user))
            
            user = request.user
            print(user, '\n\n')
            cart, _ = Cart.objects.get_or_create(user=user)
            cart_item, _ = CartItem.objects.get_or_create(product=product, cart=cart)
            
            if cart_item.quantity + quantity > product.stock:
                return Response(
                    {"error": "Quantity exceeds available stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            cart_item.quantity += quantity
            cart_item.save()
            return Response({
                'message': 'Product added to cart',
                'cart_item_quantity': cart_item.quantity,
                "product name": product.name,
                'cart total price': cart.cart_total_price,
            })
        
        
class ClearCardView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart.clear_cart()
        data = {
            'msg': "Items deleted"
        }
        return Response(
            data=data, status=status.HTTP_204_NO_CONTENT,
        )