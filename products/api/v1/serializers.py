from django.urls import reverse

from ...models import Product
from rest_framework import serializers


class  ProductSerializer(serializers.ModelSerializer):
    relative_url = serializers.ReadOnlyField(source='get_relative_url')
    # absolute_url = serializers.SerializerMethodField(method_name='get_product_absolute_url')
    
    class Meta:
        model = Product
        fields = ("name", "price", "stock", 'category', 'relative_url', 'images', )

    # def get_product_absolute_url(self, obj):
        # request = self.context.get("request")
        # if request:
            # return request.build_absolute_uri(
                # reverse('products:api-v1:product-detail', kwargs={"slug": obj.slug})                
            # )
        # else:
            # return None
        
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        return rep