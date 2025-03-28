from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from products.models import Product
from users.models import User
from decimal import Decimal



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_price(self) -> Decimal:
        return sum(item.total_price for item in self.cart_items.all())

    @property
    def item_counts(self) -> int:
        return self.cart_items.count()

    @property
    def item_names(self):
        return [item.product.name for item in self.cart_items.all()]

    def clear_cart(self):
        self.cart_items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self) -> Decimal:
        return Decimal(self.quantity) * self.product.price

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """
    Creates a new cart for the user upon registration.

    :param sender: The User model.
    :param instance: The newly created User instance.
    :param created: A boolean indicating whether the instance was newly created.
    :param kwargs: Additional keyword arguments.
    """
    if created:
        Cart.objects.get_or_create(user=instance)
