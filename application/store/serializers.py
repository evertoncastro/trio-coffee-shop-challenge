from rest_framework import serializers
from .models import Product, ProductVariation, Order


class MenuVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'name', 'price']

class MenuSerializer(serializers.ModelSerializer):
    variations = MenuVariationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'variations']


class OrderItemSerializer(serializers.Serializer):
    product_variation_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(10, 2, read_only=True)
    item_id = serializers.IntegerField(read_only=True)


class CreateOrderSerializer(serializers.Serializer):
    location = serializers.ChoiceField(choices=Order.LOCATION_CHOICES)
    order_items = OrderItemSerializer(many=True)