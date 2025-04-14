from django.urls import path
from . import views as V

from django.conf import settings


app_name = 'v1'
urlpatterns = [
    path('create-order/', V.OrderCreateView.as_view(), name='create_order'),
    path("orders_list/", V.OrdersListByUser.as_view(), name='my_orders'),
]


if settings.DEBUG:
    urlpatterns.append(path('set-order-as-paid/<uuid:order_id>/', V.SetOrderAsPaid.as_view()))