from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404

from .serializers import (UserCreationSerializer,
                          UserLoginSerializer, ProfileSerializer)
from .throttles import UserPasswordResetRequestThrottle
from ...models import Profile

class UserRegisterView(GenericAPIView):
    serializer_class = UserCreationSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "Email": serializer.validated_data['email'],
                'msg': "User created successfuly",
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


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
    