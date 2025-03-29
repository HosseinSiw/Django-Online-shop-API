from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from ...models import Cart, CartItem
from products.models import Product as pr



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            'quantity', "product", "total_price",
        )
        

class CartSerializer(serializers.ModelSerializer):
    users_username = serializers.CharField(source='user.username', read_only=True)
    users_email = serializers.CharField(source='user.email', read_only=True)
    cart_items = CartItemSerializer(many=True,)
    
    class Meta:
        model = Cart
        fields = ('cart_items', "users_username", "users_email",
                  "cart_total_price", "item_counts", "item_names", "cart_items")
        
        

class AddToCartSerializer(serializers.Serializer):
    """
    This serialzier is been developed for validation porpuses.
    """
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(_("Quantity must be grather than 0"))

    def validate_product_id(self, value):
        try:
            pr.objects.get(pk=value)
        except pr.DoesNotExist:
            raise serializers.ValidationError(_("Product does not exists currently we will charge it soon"))
        return value        
