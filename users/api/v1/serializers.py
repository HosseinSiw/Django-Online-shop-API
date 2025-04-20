from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ...models import User, Profile, LoginCode


class UserCreationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True,)
    
    class Meta:
        model = User
        fields= ("email", "username", "password1", "password",)
        extra_kwargs = {
            "password": {"write_only": True},
        }
    
    def create(self, validated_data):
        validated_data.pop('password1', None)
        user = User.objects.create_user(email=validated_data['email'], 
        password=validated_data['password'], username=validated_data['username'], )
        return user
        
    def validate(self, attrs):
        password, password1 = attrs.get("password"), attrs.get("password1")
        if not password1 == password:
            raise serializers.ValidationError(_("passwords arent match, try again."))
        
        try:
            validate_password(password=password)
        except:
            raise serializers.ValidationError(_("Password is not valid."))
        
        return super().validate(attrs)
    
    
    
# class UserLoginSerializer(TokenObtainPairSerializer):
    
#     def validate(self, attrs):
#         validated_data = super().validate(attrs)
#         validated_data['email'] = self.user.email
#         validated_data['user'] = self.user.username 
#         return validated_data
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    
class UserVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ('profile_pic', "id", "first_name", "last_name", "description", "email")
        read_only_fields = ('email', "id",)
        