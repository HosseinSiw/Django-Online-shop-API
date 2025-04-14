from rest_framework import serializers
from ...models import Order, OrderItem


class OrderCreateSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=400,)
    full_name = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=11)
    postal_code = serializers.CharField(max_length=256,)

    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    class Meta:
        model = OrderItem
        fields = ('order', "price", "product_name", "quantity",)
        read_only_fields = ('price',)
        
class OrderModelSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('order_id', "user", "user_email", "phone_number", "full_name",
                  "address", "order_status", "order_date", "postal_code", 'total_price',
                  "payment", "payment_status", "order_items", "absolute_url")
        
        read_only_fields = ('order_id', "user", "full_name",
                            "phone_number", "order_date", 'total_price')
    
    def to_representation(self, instance):
        current_rep = super().to_representation(instance)
        request = self.context.get('request')        
        order_id = request.resolver_match.kwargs.get("uuid")        
        if not order_id:
            current_rep.pop('user')
            current_rep.pop('user_email')
            current_rep.pop('payment')
            current_rep.pop('payment_status')
        else:
            current_rep.pop('absolute_url')
        
        return current_rep
    
    def get_absolute_url(self, order: Order):
        request = self.context.get("request")
        if request:
            path = f'api/v1/orders/{order.order_id}'
            return request.build_absolute_uri(path)
        return None