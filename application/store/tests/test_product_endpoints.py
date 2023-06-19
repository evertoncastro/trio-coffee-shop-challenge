from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Product, ProductVariation


class ProductVariationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        tokan: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(tokan.access_token)}')
        self.product1 = Product.objects.create(name='Product 1')
        self.product_variation1 = ProductVariation.objects.create(product=self.product1, name='Variation 1')

    def test_product_variation_list(self):
        url = reverse('product-variation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Variation 1')
