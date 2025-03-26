from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username, **extra_fields):
        if not all([username, password, email]):
            raise ValidationError("Incompelete data.")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)
