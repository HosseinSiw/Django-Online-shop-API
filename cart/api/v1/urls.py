from django.urls import path
from . import views as V


app_name = 'api-v1'

urlpatterns = [
    path("add-to-cart/<int:product_id>/", V.AddToCartView.as_view(), name='add-to-cart'),
    path('clear-cart/', V.ClearCardView.as_view(), name='cart-clear'),
]