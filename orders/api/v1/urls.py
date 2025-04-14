from django.urls import path
from . import views as V

app_name = 'v1'
urlpatterns = [
    path('create-order/', V.OrderCreateView.as_view(), name='create_order')
]