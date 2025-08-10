# mainapp/models.py

from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('pampers', 'Pampers'),
    ('soap', 'Soap'),
    ('stroller', 'Stroller'),
    ('bottle', 'Bottle'),
    ('boys', "Boy's Fashions"),
    ('girls', "Girl's Fashions"),
    ('offers', 'Offers',)
]


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)  # original price
    rating = models.IntegerField(default=0)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    free_shipping = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage

    # New fields
    highlight_text = models.TextField(blank=True)
    description = models.TextField(blank=True)    

    def discount_price(self):
        return self.mrp - self.price

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/multiple/')

    def __str__(self):
        return f"{self.product.name} - Extra Image"


class CartItem(models.Model):
    """
    Stores cart items for both logged-in and guest users.
    - If user is logged in: store in `user` field.
    - If guest: store in `session_key`.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, db_index=True, blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
