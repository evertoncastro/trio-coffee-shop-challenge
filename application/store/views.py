from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Product, ProductVariation, Order, OrderItem
from .serializers import MenuSerializer, CreateOrderSerializer


class MenuView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Product.objects.filter(active=True).prefetch_related(
            Prefetch('variations', queryset=ProductVariation.objects.filter(active=True))
        )
    

class OrderCreateView(generics.CreateAPIView):
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