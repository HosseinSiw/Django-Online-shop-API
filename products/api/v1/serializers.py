from django.urls import reverse
from rest_framework import serializers
from ...models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'id', "image"
        )

class  ProductSerializer(serializers.ModelSerializer):
    relative_url = serializers.ReadOnlyField(source='get_relative_url')
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='get_category_name')
    absolute_url = serializers.SerializerMethodField(method_name='get_product_absolute_url')
    
    class Meta:
        model = Product
        fields = ('id', "name", "price", "stock", 'relative_url', 'images', 'absolute_url', "category_name")

    def get_product_absolute_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(
                reverse('products:api-v1:product-details', kwargs={"slug": obj.slug})                
            )
        else:
            return None
        
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        request = self.context.get('request')
        if request:
            slug = request.parser_context.get("kwargs", {}).get('slug') if request and request.parser_context else None
            if slug is not None:
                rep.pop("absolute_url", None)
                rep.pop("relative_url", None)
            else:
                rep = rep
        return rep
    
    