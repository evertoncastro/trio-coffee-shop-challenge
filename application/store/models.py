from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=255)
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

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)