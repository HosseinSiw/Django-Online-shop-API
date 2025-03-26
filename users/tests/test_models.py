from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import User  


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active) 
        self.assertFalse(user.is_staff) 
        self.assertFalse(user.is_superuser)  

    def test_email_is_required(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email="",
                username="testuser",
                password="testpass123"
            )

    def test_username_is_unique(self):
        User.objects.create_user(
            email="test1@example.com",
            username="testuser",
            password="testpass123"
        )
        with self.assertRaises(Exception): 
            User.objects.create_user(
                email="test2@example.com",
                username="testuser",  # Duplicate username
                password="testpass123"
            )