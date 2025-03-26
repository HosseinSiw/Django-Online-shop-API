from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.test import APITestCase
from ..api.v1.serializers import UserCreationSerializer, UserLoginSerialier
from django.utils.translation import gettext_lazy as _
from ..models import User


class UserCreationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'SecurePass123!',
            'password1': 'SecurePass123!'
        }

    def test_valid_serializer_data(self):
        serializer = UserCreationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    
    def test_password_mismatch_validation(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password1'] = 'WrongPass123!'
        serializer = UserCreationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            _("passwords arent match, try again.")
        )
    
    def test_weak_password_validation(self):
        weak_password_data = self.valid_data.copy()
        weak_password_data['password'] = '123'
        weak_password_data['password1'] = '123'
        serializer = UserCreationSerializer(data=weak_password_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            _("Password is not valid.")
        )
    
    def test_missing_required_fields(self):
        incomplete_data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!'
            # Missing username and password1
        }
        serializer = UserCreationSerializer(data=incomplete_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('password1', serializer.errors)
    
    def test_create_user_method(self):
        serializer = UserCreationSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertEqual(user.email, self.valid_data['email'])
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertTrue(user.check_password(self.valid_data['password']))
        self.assertFalse(hasattr(user, 'password1'))  # password1 should be removed

    def test_password1_not_in_output(self):
        serializer = UserCreationSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serialized_data = serializer.data
        self.assertNotIn('password1', serialized_data)
        self.assertNotIn('password', serialized_data)  # passwords should never be in output

