from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.db import transaction


from payments.models import PaymentModel as Payment
from cart.models import Cart
from ...models import Order, OrderItem    
from .serializers import OrderCreateSerializer, OrderModelSerializer
from .paginators import OrderPaginator
from .permissions import IsOwnerOrReadOnly


class OrderCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer
    
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
                
            response_data = OrderModelSerializer(order, context={'request': request})
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetOrderAsPaid(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    """
    This view is for debuging purposes.
    """
    def post(self, request, order_id):
        if settings.DEBUG:
            order = Order.objects.get(order_id=order_id)
            order.payment.status = "S" # Success.
            order.order_status = "Pr"  # Processing.  
            order.save()
            return Response({
                'Order id': order_id,
                "Status": order.order_status,
                'full_name': order.full_name,
            }, status=status.HTTP_200_OK)
        else:
            pass
        
        
class OrdersListByUser(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = OrderModelSerializer
    pagination_class = OrderPaginator
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]    
    filterset_fields = ['order_status',]
    ordering_fields = ['order_date', 'total_amount']
    ordering = ['-order_date']
    search_fields = ['order_items__product__name', "total_amount", "order_status",]
    
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        
        orders = orders.prefetch_related(
            Prefetch('order_items', queryset=OrderItem.objects.select_related('product'))
        )
        return orders
    
    
class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]  # My custom permission class.
    serializer_class = OrderModelSerializer
    
    def get(self, request, order_id):
        order = Order.objects.get(order_id=order_id)
        serializer = self.serializer_class(order, context={'request': request})
        return Response(
            data=serializer.data, status=status.HTTP_200_OK,
        )
        