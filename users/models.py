from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractBaseUser, PermissionsMixin):
    # Personal Information
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    # Permissions

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Dating Information
    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username + " " + self.email

    def has_perm(self, perm, obj = ...):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.has_module_perms
    

class Profile(models.Model):
    """
    The Profile table. (model)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_owner')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='users/profile_pics')
    description = models.CharField(max_length=256)
    
    def __str__(self):
        msg = f'{self.user.username} - Profile'
        return msg
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

