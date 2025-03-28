from ...models import Product
from .serializers import ProductSerializer
from .paginators import ProdcutPaginator

from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions


class ProductListView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny,]
    pagination_class = ProdcutPaginator
    
        
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny,]
    
    