import random

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage

from .serializers import (UserCreationSerializer,
                          UserLoginSerializer, ProfileSerializer, UserVerifySerializer)
from .throttles import UserPasswordResetRequestThrottle, UserRegisterationThrottle
from ...models import User, Profile, LoginCode
from users.utils.email import EmailThread
from users.utils.security import get_ip_from_request, track_login_failure, reset_login_attemps


class UserRegisterView(GenericAPIView):
    serializer_class = UserCreationSerializer
    throttle_classes = [UserRegisterationThrottle,]
    
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            code = random.randint(100000, 999999)
            email = serializer.validated_data['email']
            LoginCode.objects.create(
                email=email,
                code = code,
            )
            
            email_obj = EmailMessage('email/active.tpl',
                                     {'mail': email, "code": code},
                                     "admin@admin.com",
                                     to=[email])
            EmailThread(email=email_obj).start()
            
            response_data = {
                "Email": email,
                'msg': "User created successfuly, please verify your account and continue",
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserVerifyView(GenericAPIView):
    serializer_class = UserVerifySerializer

    def post(self, request,):
        code = request.data['code']
        code = LoginCode.objects.filter(code=code).first()
        if not code:
            return Response({"code": "Code not found"}, 400)
        if code.is_used == True or code.validate_code() == False:
            return Response({"code": "The code is deprecated"}, 400)
        email = code.email
        user = User.objects.filter(email=email)
        if not user:
            return Response({"msg": "User not found"}, 400)
        user.is_verified = True
        user.save()
        code.delete()
        data = {
            "Msg": "Your account has been verified"
        }
        return Response(data=data, status=status.HTTP_200_OK)
                
class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        ip = get_ip_from_request(request=request)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['passowrd']
            
            user = authenticate(email=email, passowrd=password)
            if not user:
                track_login_failure(ip)
                return Response({"msg": "Invalid data"}, status=status.HTTP_401_UNAUTHORIZED)
            
            reset_login_attemps(ip)
            token = RefreshToken.for_user(user)
            data = {
                'email': email,
                'access_token': str(token.access_token),
                "refresh_token": str(token),
            }
            return Response(data=data, status=status.HTTP_200_OK)
        
        track_login_failure(ip)
        return Response({"msg": "Invalid data"}, 
                        status=status.HTTP_400_BAD_REQUEST)

'''
Todo: Done the password related endpoints when the docker setup completed (due to smpt4dev)
class UserPasswordResetRequestView(APIView):
    throttle_classes = UserPasswordResetRequestThrottle
    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        pass
'''


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Profile.objects.all()
    
    def get_object(self):
        queryset = self.get_queryset()
        profile = get_object_or_404(queryset, user=self.request.user)    
        return profile
    