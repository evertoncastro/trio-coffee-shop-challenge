from rest_framework import serializers
from .models import Product, ProductVariation


class MenuVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'name']

class MenuSerializer(serializers.ModelSerializer):
    variations = MenuVariationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'variations']