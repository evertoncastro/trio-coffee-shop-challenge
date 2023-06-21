from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Product, ProductVariation, Order, OrderItem, Customer
from ..serializers import OrderDetailModelSerializer, CreateOrderSerializer


class OrderCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
    
    def test_create_order(self):
        product1 = Product.objects.create(name='Product 1', active=True)
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
        product1 = Product.objects.create(name='Product 1', active=True)
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

    def test_create_order_item_for_order_with_status_different_than_waiting(self):
        # Test creating an order item with for order with status different than waiting
        order: Order = Order.objects.create(customer=self.customer, location='in_house', status=Order.PREPARATION)
        payload = {
            'quantity': 3,
            'item_id': self.product_variation.id
        }

        url = reverse('order-item-create', args=[order.id])
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {'detail': 'The order cannot be modified when it is not in waiting status.'}
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
        self.product: Product = Product.objects.create(name='Product 1', active=True)
        self.product_variation = ProductVariation.objects.create(product=self.product, name='Test Product Variation', active=True, price=10.0)
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

    def test_patch_order_item_as_different_customer(self):
        # Create order with a different customer than the one authenticated
        other_user: User = User.objects.create_user(username='otheruser', password='testpassword')
        other_customer: Customer = Customer.objects.create(user=other_user)
        order: Order = Order.objects.create(customer=other_customer, location='in_house')
        order_item = OrderItem.objects.create(order=order, item_id=self.product_variation.pk, quantity=2, price=10.0)

        # Send a PATCH request to update the order item
        data = {'quantity': 5}
        url = reverse('order-item-update-delete', args=[order.id, order_item.id])
        response = self.client.patch(url, data)

        # Verify the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_item_quantity_for_order_with_status_different_than_waiting(self):
        # Test updating the quantity of an order with status different than waiting
        order: Order = Order.objects.create(customer=self.customer, location='in_house', status=Order.PREPARATION)
        order_item: OrderItem = OrderItem.objects.create(order=order, item_id=self.product_variation.pk, quantity=2, price=10.0)
        payload = {'quantity': 1}
        url = reverse('order-item-update-delete', args=[order.id, order_item.id])
        response = self.client.patch(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {'detail': 'The order cannot be modified when it is not in waiting status.'}
        )


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
        product1: Product = Product.objects.create(name='Product 1', active=True)
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

    def test_delete_order_item_as_different_customer(self):
        # Create order with a different customer than the one authenticated
        other_user: User = User.objects.create_user(username='otheruser', password='testpassword')
        other_customer: Customer = Customer.objects.create(user=other_user)
        order: Order = Order.objects.create(customer=other_customer, location='in_house')
        order_item = OrderItem.objects.create(order=order, item_id=self.product_variation.pk, quantity=2, price=10.0)

        # Send a delete request to update the order item
        url = reverse('order-item-update-delete', args=[order.id, order_item.id])
        response = self.client.delete(url)

        # Verify the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_item_for_order_with_status_different_than_waiting(self):
        # Test delete order item for order with status different than waiting
        order: Order = Order.objects.create(customer=self.customer, location='in_house', status=Order.PREPARATION)
        order_item: OrderItem = OrderItem.objects.create(order=order, item_id=self.product_variation.pk, quantity=2, price=10.0)
        url = reverse('order-item-update-delete', args=[order.id, order_item.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {'detail': 'The order cannot be modified when it is not in waiting status.'}
        )


class OrderDetailViewTestCase(APITestCase):
    def setUp(self):
        # Create the user and authentication
        self.user: User = User.objects.create_user(username='testuser', password='testpassword')
        token: RefreshToken = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token.access_token)}')
        self.customer: Customer = Customer.objects.create(user=self.user)

        # Create a test order
        self.order: Order = Order.objects.create(customer=self.customer, location='in_house')

        # Create a test order item
        product: Product = Product.objects.create(name='Product 1', active=True)
        self.product_variation: ProductVariation = ProductVariation.objects.create(product=product, name='Test Product Variation', active=True, price=10.0)
        self.order_item = OrderItem.objects.create(order=self.order, item_id=self.product_variation.pk, quantity=2, price=10.0)
        
    def test_get_order_details(self):
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.get(url)
        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert response data
        expected_data = OrderDetailModelSerializer(instance=self.order).data
        self.assertEqual(response.data, expected_data)

    def test_get_order_details_invalid_order_id(self):
        url = reverse('order-detail', args=[9999])
        response = self.client.get(url)
        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_details_total_price(self):
        # Calculate the expected total price
        total_price = self.product_variation.price * self.order_item.quantity
        
        url = reverse('order-detail', args=[self.order.id])
        response = self.client.get(url)
        # Assert response data
        self.assertEqual(response.data['total_price'], total_price)
