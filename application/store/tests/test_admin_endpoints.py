from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Product, ProductVariation
from ..serializers.admin_serializers import ProductSerializer

class ProductCreateViewTestCase(APITestCase):
    
    def test_create_product_with_variations(self):
        product_data = {
            'name': 'Product 1',
            'active': True,
            'variations': [
                {
                    'name': 'Variation 1',
                    'price': 10.0,
                    'active': True
                },
                {
                    'name': 'Variation 2',
                    'price': 15.0,
                    'active': True
                }
            ]
        }

        url = reverse('admin-create-product')
        response = self.client.post(url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(ProductVariation.objects.count(), 2)
        product = Product.objects.get()
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)

    def test_create_product_with_no_variation_creates_a_default_variation_automatically(self):
        product_data = {
            'name': 'Product 1',
            'active': True
        }

        url = reverse('admin-create-product')
        response = self.client.post(url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(ProductVariation.objects.count(), 1)
        product = Product.objects.get()
        self.assertEqual(product.variations.all()[0].name, '-')
        self.assertFalse(product.variations.all()[0].active)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
