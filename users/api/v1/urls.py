from django.urls import path
from users.api.v1 import views

from rest_framework_simplejwt.views import (
    TokenVerifyView, TokenRefreshView
)

app_name = 'api-v1'

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name='register'),

    # login JWT
    path("jwt/create/", views.UserLoginView.as_view(), name='jwt_create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),
    
    # Profile related endpoints
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
