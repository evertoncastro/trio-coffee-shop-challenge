from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOrderItemCustomer
from .mixins import MultipleFieldLookupMixin
from .models import Customer, Product, ProductVariation, Order, OrderItem
from .serializers import MenuModelSerializer, CreateOrderSerializer, CreateOrderItemModelSerializer, UpdateOrderItemModelSerializer


class MenuView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuModelSerializer

    def get_queryset(self):
        return Product.objects.filter(active=True).prefetch_related(
            Prefetch('variations', queryset=ProductVariation.objects.filter(active=True))
        )
    

class CreateOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = request.data.get('location')
        order_items = request.data.get('order_items', [])

        customer, _ = Customer.objects.get_or_create(user=request.user)
        order = Order.objects.create(customer=customer, location=location)
        product_variation_ids = [line['product_variation_id'] for line in order_items]
        product_variations = ProductVariation.objects.filter(id__in=product_variation_ids)
        product_variations_mapping = {variation.id: variation for variation in product_variations}

        order_item_models = []
        for line in order_items:
            variation_id = line['product_variation_id']
            quantity = line['quantity']
            variation = product_variations_mapping.get(variation_id)
            if not variation:
                return Response(
                    {'error': f'ProductVariation with id {variation_id} does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            order_item_models.append(
                OrderItem(order=order, name=variation.name,
                price=variation.price, quantity=quantity,
                item_id=variation.id)
            )

        OrderItem.objects.bulk_create(order_item_models)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CreateOrderItemView(generics.CreateAPIView):
    serializer_class = CreateOrderItemModelSerializer
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        return Order.objects.filter(id=order_id)

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        serializer.save(order=order)


class UpdateDeleteOrderItemView(MultipleFieldLookupMixin, generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOrderItemCustomer]
    serializer_class = UpdateOrderItemModelSerializer
    queryset = OrderItem.objects.all()
    lookup_fields = ('id', 'order_id')

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
