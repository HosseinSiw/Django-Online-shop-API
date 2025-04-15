from django.urls import path, include


app_name = 'payments'
urlpatterns = [
    path('api-v1/', include('payments.api.v1.urls'), name='api-v1'),
    path("api-v2/", include('payment.api.v2.urls'), name='api-v2')
]