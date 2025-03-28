from django.urls import path
from . import views as v


app_name = 'api-v1'

urlpatterns = [
    path('product-list', v.ProductListView.as_view(), name='product-list'),
]
