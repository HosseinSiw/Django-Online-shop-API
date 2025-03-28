from decimal import Decimal
from django.test import TestCase
from users.models import User
from cart.models import Cart, CartItem


class TestCartModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@email.com',
            password='123456/test',
            username = 'test'
        )
        
    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.item_counts, 0)
        self.assertEqual(cart.total_price, Decimal(0))
        self.assertEqual(cart.item_names, [])