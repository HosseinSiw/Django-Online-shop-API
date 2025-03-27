from django.test import TestCase
from decimal import Decimal
from ..models import Category, Product, ProductImage


class ProductModelsTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='testing')
        
        self.assertEqual(Category.objects.all()[0].name, category.name)
        self.assertEqual(len(Category.objects.all()), 1)
        
    def test_product_creation(self):
        cat = Category.objects.create(name='sample')
        product = Product.objects.create(
            name='test product',
            price=Decimal('100.5'),
            stock=10,
            category=cat,
        )
        self.assertEqual(product.name, Product.objects.get(pk=1).name)
        self.assertIsNotNone(product.slug)
        self.assertEqual(product.price, Product.objects.get(pk=1).price)
        self.assertEqual(product.stock, Product.objects.get(pk=1).stock)
    
    def test_product_model_methods(self):
        name = 'test product'
        cat = Category.objects.create(name='sample')
        product = Product.objects.create(
            price=Decimal('100.5'),
            stock=10,
            category=cat,
        )
        self.assertEqual(product.get_category_name(), 'sample')
        self.assertEqual(str(product), product.name)
        
    