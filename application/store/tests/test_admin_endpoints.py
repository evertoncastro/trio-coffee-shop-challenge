from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Product, ProductVariation
from ..serializers.admin_serializers import ProductSerializer


class ProductCreateViewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', is_superuser=True, is_staff=True)
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
    
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

        url = reverse('admin-product-create')
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

        url = reverse('admin-product-create')
        response = self.client.post(url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(ProductVariation.objects.count(), 1)
        product = Product.objects.get()
        self.assertEqual(product.variations.all()[0].name, '-')
        self.assertFalse(product.variations.all()[0].active)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)


class ProductUpdateViewTestCase(APITestCase):
    
    def setUp(self):
      self.user = User.objects.create_user(
          username='testuser', password='testpassword', is_superuser=True, is_staff=True)
      token: RefreshToken = RefreshToken.for_user(self.user)
      self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
      self.product = Product.objects.create(name='Product 1', active=True)
      self.variation1 = ProductVariation.objects.create(product=self.product, name='Variation 1', price=10.0, active=True)
      self.variation2 = ProductVariation.objects.create(product=self.product, name='Variation 2', price=15.0, active=True)

    def test_update_product_and_variations(self):
        # Define the updated product and variation data
        updated_data = {
            'name': 'Updated Product',
            'active': False,
            'variations': [
                {
                    'id': self.variation1.id,
                    'name': 'Updated Variation 1',
                    'price': 12.0,
                    'active': False
                },
                {
                    'name': 'New Variation',
                    'price': 20.0,
                    'active': True
                }
            ]
        }

        # Define the URL for updating the product
        url = reverse('admin-product-update', kwargs={'pk': self.product.id})
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.product.refresh_from_db()
        self.variation1.refresh_from_db()
        self.variation2.refresh_from_db()

        self.assertEqual(self.product.variations.count(), 3)

        # Assert that the product and variation fields are updated correctly
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.active, False)
        self.assertEqual(self.variation1.name, 'Updated Variation 1')
        self.assertEqual(self.variation1.price, 12.0)
        self.assertEqual(self.variation1.active, False)

        # Assert that a new variation is created
        new_variation = ProductVariation.objects.get(name='New Variation')
        self.assertEqual(new_variation.product, self.product)
        self.assertEqual(new_variation.price, 20.0)
        self.assertEqual(new_variation.active, True)