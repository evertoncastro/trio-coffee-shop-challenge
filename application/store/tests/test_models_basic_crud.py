from django.contrib.auth.models import User
from django.test import TestCase
from application.store.models import Customer, Product, ProductVariation, Order, OrderItem


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user)

    # Customer Model Tests

    def test_customer_creation(self):
        self.assertEqual(Customer.objects.count(), 1)

    def test_customer_retrieval(self):
        retrieved_customer = Customer.objects.get(pk=self.customer.id)
        self.assertEqual(retrieved_customer, self.customer)

    def test_customer_update(self):
        self.customer.user.first_name = 'Updated First Name'
        self.customer.user.save()
        updated_customer = Customer.objects.get(pk=self.customer.id)
        self.assertEqual(updated_customer.user.first_name, 'Updated First Name')

    def test_customer_deletion(self):
        self.customer.delete()
        self.assertEqual(Customer.objects.count(), 0)

    # Product Model Tests

    def test_product_creation(self):
        product = Product.objects.create(name='Test Product', active=True)
        self.assertEqual(product.name, 'Test Product')
        self.assertTrue(product.active)
        self.assertIsNotNone(product.date_created)
        self.assertIsNotNone(product.date_updated)

    def test_product_retrieval(self):
        product = Product.objects.create(name='Test Product', active=True)
        retrieved_product = Product.objects.get(pk=product.id)
        self.assertEqual(retrieved_product, product)

    def test_product_update(self):
        product = Product.objects.create(name='Test Product', active=True)
        product.name = 'Updated Product'
        product.active = False
        product.save()
        updated_product = Product.objects.get(pk=product.id)
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertFalse(updated_product.active)

    def test_product_deletion(self):
        product = Product.objects.create(name='Test Product', active=True)
        product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=product.id)

    # ProductVariation Model Tests

    def test_product_variation_creation(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        self.assertEqual(variation.product, product)
        self.assertEqual(variation.name, 'Variation 1')
        self.assertTrue(variation.active)
        self.assertIsNotNone(variation.date_created)
        self.assertIsNotNone(variation.date_updated)

    def test_product_variation_retrieval(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        retrieved_variation = ProductVariation.objects.get(pk=variation.id)
        self.assertEqual(retrieved_variation, variation)

    def test_product_variation_update(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        variation.name = 'Updated Variation'
        variation.active = False
        variation.save()
        updated_variation = ProductVariation.objects.get(pk=variation.id)
        self.assertEqual(updated_variation.name, 'Updated Variation')
        self.assertFalse(updated_variation.active)

    def test_product_variation_deletion(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        variation.delete()
        with self.assertRaises(ProductVariation.DoesNotExist):
            ProductVariation.objects.get(pk=variation.id)

    # Order Model Tests

    def test_order_creation(self):
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.location, 'in_house')
        self.assertEqual(order.status, 'waiting')

    def test_order_retrieval(self):
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        retrieved_order = Order.objects.get(pk=order.id)
        self.assertEqual(retrieved_order, order)

    def test_order_update(self):
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        order.status = 'preparation'
        order.save()
        updated_order = Order.objects.get(pk=order.id)
        self.assertEqual(updated_order.status, 'preparation')

    def test_order_deletion(self):
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        order.delete()
        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(pk=order.id)

    # OrderItem Model Tests

    def test_order_item_creation(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        order_item = OrderItem.objects.create(order=order, product_variation=variation)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product_variation, variation)

    def test_order_item_retrieval(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        order_item = OrderItem.objects.create(order=order, product_variation=variation)
        retrieved_order_item = OrderItem.objects.get(pk=order_item.id)
        self.assertEqual(retrieved_order_item, order_item)

    def test_order_item_update(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation1 = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        variation2 = ProductVariation.objects.create(product=product, name='Variation 2', active=True)
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        order_item = OrderItem.objects.create(order=order, product_variation=variation1)
        order_item.product_variation = variation2
        order_item.save()
        updated_order_item = OrderItem.objects.get(pk=order_item.id)
        self.assertEqual(updated_order_item.product_variation, variation2)

    def test_order_item_deletion(self):
        product = Product.objects.create(name='Test Product', active=True)
        variation = ProductVariation.objects.create(product=product, name='Variation 1', active=True)
        order = Order.objects.create(customer=self.customer, location='in_house', status='waiting')
        order_item = OrderItem.objects.create(order=order, product_variation=variation)
        order_item.delete()
        with self.assertRaises(OrderItem.DoesNotExist):
            OrderItem.objects.get(pk=order_item.id)
