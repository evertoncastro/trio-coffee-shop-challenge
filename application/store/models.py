from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class Order(models.Model):
    LOCATION_CHOICES = [
        ('in_house', 'In House'),
        ('take_away', 'Take Away'),
    ]
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('preparation', 'Preparation'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    item_id = models.IntegerField(null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
