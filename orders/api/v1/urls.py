from django.urls import path
from . import views as V

from django.conf import settings


app_name = 'v1'
urlpatterns = [
    path('create-order/', V.OrderCreateView.as_view(), name='create_order'),
    path("orders/", V.OrdersListByUser.as_view(), name='orders_list'),
    path("orders/<uuid:order_id>/", V.OrderDetailView.as_view(), name='order_details'),
]


if settings.DEBUG:
    urlpatterns.append(path('set-order-as-paid/<uuid:order_id>/', V.SetOrderAsPaid.as_view()))