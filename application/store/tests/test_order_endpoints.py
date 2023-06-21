from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Product, ProductVariation, Order, OrderItem, Customer
from rest_framework_simplejwt.tokens import RefreshToken


class OrderCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
    
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


class CreateOrderItemViewTestCase(APITestCase):
    def setUp(self):
        # Create the user and authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
        self.customer = Customer.objects.create(user=self.user)

        # Create a test order
        self.order = Order.objects.create(customer=self.customer, location='in_house')
        self.order_url = reverse('order-item-create', args=[self.order.id])

        # Create a test product variation
        product1 = Product.objects.create(name='Product 1', price=10.00, active=True)
        self.product_variation = ProductVariation.objects.create(
            product=product1, name='Test Product Variation', active=True, price=10
        )

    def test_create_order_item_success(self):
        # Test creating a new order item
        payload = {
            'quantity': 2,
            'item_id': self.product_variation.id
        }

        response = self.client.post(self.order_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_item = OrderItem.objects.last()
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.item_id, self.product_variation.pk)
        self.assertEqual(order_item.quantity, payload['quantity'])

    def test_create_order_item_non_existing_variation(self):
        # Test creating an order item with a non-existing product variation
        payload = {
            'quantity': 3,
            'item_id': 0  # Non-existing product variation ID
        }

        response = self.client.post(self.order_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['ProductVariation with id 0 does not exist.'])

    def test_create_order_item_duplicate_item(self):
        # Test creating an order item with an item ID that already exists in the order
        OrderItem.objects.create(order=self.order, item_id=self.product_variation.pk, quantity=2, price=10.0)
        payload = {
            'quantity': 3,
            'item_id': self.product_variation.id
        }

        response = self.client.post(self.order_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'non_field_errors': [f'OrderItem with item_id {self.product_variation.id} already exists in the order.']}
        )


class OrderItemUpdateViewTestCase(APITestCase):
    def setUp(self):
        # Create the user and authentication
        self.user: User = User.objects.create_user(username='testuser', password='testpassword')
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
        self.customer: Customer = Customer.objects.create(user=self.user)

        # Create a test order
        self.order: Order = Order.objects.create(customer=self.customer, location='in_house')

        # Create a test order item
        product1: Product = Product.objects.create(name='Product 1', price=10.00, active=True)
        self.product_variation = ProductVariation.objects.create(product=product1, name='Test Product Variation', active=True, price=10.0)
        self.order_item = OrderItem.objects.create(order=self.order, item_id=self.product_variation.pk, quantity=2, price=10.0)
        self.order_item_url = reverse('order-item-update-delete', args=[self.order.id, self.order_item.id])

    def test_update_order_item_quantity_success(self):
        # Test updating the quantity of an existing order item
        payload = {'quantity': 5}
        response = self.client.patch(self.order_item_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_item = OrderItem.objects.get(id=self.order_item.id)
        self.assertEqual(order_item.quantity, payload['quantity'])

    def test_update_order_item_quantity_non_existing_item(self):
        # Test updating the quantity of a non-existing order item 999
        invalid_order_item_url = reverse('order-item-update-delete', args=[self.order.id, 999])
        payload = {'quantity': 5}
        response = self.client.patch(invalid_order_item_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_item_quantity_non_existing_order(self):
        # Test updating the quantity of a non-existing order 999
        invalid_order_item_url = reverse('order-item-update-delete', args=[999, self.order_item.id])
        payload = {'quantity': 5}
        response = self.client.patch(invalid_order_item_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_item_quantity_invalid_quantity(self):
        # Test updating the quantity of an order item with an invalid quantity 0
        payload = {'quantity': 0}
        response = self.client.patch(self.order_item_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['quantity'][0], 'Ensure this value is greater than or equal to 1.')


class OrderItemDeleteViewTestCase(APITestCase):
    def setUp(self):
        # Create the user and authentication
        self.user: User = User.objects.create_user(username='testuser', password='testpassword')
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
        self.customer: Customer = Customer.objects.create(user=self.user)

        # Create a test order
        self.order: Order = Order.objects.create(customer=self.customer, location='in_house')

        # Create a test order item
        product1: Product = Product.objects.create(name='Product 1', price=10.00, active=True)
        self.product_variation: ProductVariation = ProductVariation.objects.create(product=product1, name='Test Product Variation', active=True, price=10.0)
        self.order_item = OrderItem.objects.create(order=self.order, item_id=self.product_variation.pk, quantity=2, price=10.0)
        self.order_item_url = reverse('order-item-update-delete', args=[self.order.id, self.order_item.id])

    def test_delete_order_item_success(self):
        # Test deleting an existing order item
        response = self.client.delete(self.order_item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the order item is deleted
        self.assertFalse(OrderItem.objects.filter(id=self.order_item.id).exists())

    def test_delete_order_item_non_existing_item(self):
        # Test deleting a non-existing order item 999
        invalid_order_item_url = reverse('order-item-update-delete', args=[self.order.id, 999])
        response = self.client.delete(invalid_order_item_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_item_non_existing_order(self):
        # Test deleting an order item from a non-existing order 999
        invalid_order_item_url = reverse('order-item-update-delete', args=[999, self.order_item.id])
        response = self.client.delete(invalid_order_item_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
