from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product, Category
from cart.models import Cart, CartItem
from decimal import Decimal


User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpass", email='test@test.com')
        
        # Create products
        self.category_1 = Category.objects.create(name='test_category_1')
        self.category_2 = Category.objects.create(name='test_category_2')
        self.product1 = Product.objects.create(name="Laptop", price=Decimal("1000.00"), stock=10, category=self.category_1)
        self.product2 = Product.objects.create(name="Mouse", price=Decimal("50.00"), stock=20, category=self.category_2)

        # Retrieve the auto-created cart for the user
        self.cart = Cart.objects.get(user=self.user)

    def test_cart_created_for_new_user(self):
        """Test that a cart is automatically created for a new user."""
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.cart.user, self.user)

    def test_add_items_to_cart(self):
        """Test adding items to the cart and updating quantity."""
        cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)

        self.assertEqual(CartItem.objects.count(), 2)
        self.assertEqual(cart_item1.total_price, Decimal("2000.00"))
        self.assertEqual(cart_item2.total_price, Decimal("150.00"))

    def test_cart_total_price(self):
        """Test cart total price calculation."""
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)  # 1000 * 2
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)  # 50 * 3

        self.assertEqual(self.cart.cart_total_price, Decimal("2150.00"))

    def test_clear_cart(self):
        """Test clearing the cart."""
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)

        self.assertEqual(self.cart.item_counts, 2)
        self.cart.clear_cart()
        self.assertEqual(self.cart.item_counts, 0)
