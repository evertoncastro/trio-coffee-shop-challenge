from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from ..models import Product, ProductVariation
from rest_framework_simplejwt.tokens import RefreshToken


class MenuViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        tokan: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(tokan.access_token)}")

    def test_menu_view(self):
        product1 = Product.objects.create(name="Product 1", active=True)
        variation1 = ProductVariation.objects.create(
            product=product1, name="Variation 1", price=12.00, active=True
        )
        ProductVariation.objects.create(
            product=product1, name="Variation 2", price=15.00, active=False
        )

        product2 = Product.objects.create(name="Product 2", active=True)
        variation3 = ProductVariation.objects.create(
            product=product2, name="Variation 3", price=10.00, active=True
        )

        url = reverse("menu")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        product_data1 = response.data[0]
        self.assertEqual(product_data1["id"], 1)
        self.assertEqual(product_data1["name"], product1.name)
        self.assertEqual(len(product_data1["variations"]), 1)

        variation_data1 = product_data1["variations"][0]
        self.assertEqual(variation_data1["id"], 1)
        self.assertEqual(variation_data1["name"], variation1.name)
        self.assertEqual(variation_data1["price"], variation1.price)

        product_data2 = response.data[1]
        self.assertEqual(product_data2["id"], 2)
        self.assertEqual(product_data2["name"], product2.name)
        self.assertEqual(len(product_data2["variations"]), 1)

        variation_data3 = product_data2["variations"][0]
        self.assertEqual(variation_data3["id"], 3)
        self.assertEqual(variation_data3["name"], variation3.name)
        self.assertEqual(variation_data3["price"], variation3.price)
