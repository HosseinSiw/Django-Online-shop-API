from django.urls import path
from . import views as v


app_name = 'api-v1'

urlpatterns = [
    path('products/', v.ProductListView.as_view(), name='product-list'),
    path("products/<slug:slug>/", v.ProductDetailView.as_view(), name='product-details')
]
