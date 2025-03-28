from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.template.defaultfilters import slugify


class Category(models.Model):
    """
    The product category Table.
    """
    name = models.CharField(max_length=30, unique=True, blank=False, null=False)
    
    
class Product(models.Model):
    """
    The main Product Table.
    """
    name = models.CharField(max_length=100, null=False, blank=False,)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="fashion")
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=150, null=False, blank=False, unique=True)
    
    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.name or self.name == "":
            raise ValidationError("Name is required")
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_category_name(self):
        return self.category.name
    
    def get_relative_url(self):
        return f'/products/{self.slug}/'
    
    
class ProductImage(models.Model):
    """
    This model will represent the Images of each product.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"
    
