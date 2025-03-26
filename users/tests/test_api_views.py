from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from ..models import User


class TestUsersAPIEndPoints(APITestCase):
    def setUp(self):
        self.register_url = reverse('users:api-v1:register')
        self.client = APIClient()
    
    # 1. Test successful registration
    def test_registeration_with_valid_data(self):
        valid_data = {
        "email": "unique_email@email.com",
        "username": "testuser",
        "password": "SecurePass123!@#",
        "password1": "SecurePass123!@#",
        }
        response = self.client.post(path=self.register_url, data=valid_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(User.objects.get().username, valid_data['username'])
        
    def test_registeration_with_invalid_email(self):
        data = {
            'email': "email",
            'username': "inv username",
            'passowrd': "1234/test",
            'password1': "1234/test",
        }
        response = self.client.post(path=self.register_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_without_required_fields(self):
        data = {
            'email': "email@incom.com"
        }
        response = self.client.post(path=self.register_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)