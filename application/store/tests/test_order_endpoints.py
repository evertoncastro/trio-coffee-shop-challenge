from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Product, ProductVariation, Order
from rest_framework_simplejwt.tokens import RefreshToken


class OrderCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        tokan: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(tokan.access_token)}')
    
    def test_create_order(self):
        product1 = Product.objects.create(name='Product 1', price=10.00, active=True)
        product_variation = ProductVariation.objects.create(product=product1, name='Product Variation 1', price=10.0)
        order_data = {
            'location': 'in_house',
            'order_items': [
                {
                    'product_variation_id': product_variation.id,
                    'quantity': 2
                }
            ]
        }

        url = reverse('order')
        response = self.client.post(url, order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.last()
        self.assertEqual(order.customer.user, self.user)
        self.assertEqual(order.location, 'in_house')
        self.assertEqual(order.order_items.count(), 1)
        
        order_item = order.order_items.first()
        self.assertEqual(order_item.name, product_variation.name)
        self.assertEqual(order_item.price, product_variation.price)
        self.assertEqual(order_item.quantity, 2)
