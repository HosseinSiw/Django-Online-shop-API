from ...models import Product
from .serializers import ProductSerializer
from .paginators import ProdcutPaginator
from .throttles import ProductEndpointsThrottle

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


@method_decorator(cache_page(60 * 10), name='get')
class ProductListView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny,]
    pagination_class = ProdcutPaginator
    throttle_classes = [ProductEndpointsThrottle,]
    
        
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    throttle_classes = [ProductEndpointsThrottle,]

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        raise PermissionDenied(detail='Only super users can update products')
    
    def get_permissions(self):
        if self.request.method in ['PUT', "PATCH", 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        raise PermissionDenied(detail='You dont have perm to delete a product')
    