from rest_framework import serializers
from ..models import Product, ProductVariation
from collections import OrderedDict


class ProductVariationSerializer(serializers.ModelSerializer):
    date_created = serializers.CharField(read_only=True)
    date_updated = serializers.CharField(read_only=True)

    class Meta:
        model = ProductVariation
        fields = ['name', 'price', 'active', 'date_created', 'date_updated']

class ProductSerializer(serializers.ModelSerializer):
    variations = ProductVariationSerializer(many=True, required=False)
    date_created = serializers.CharField(read_only=True)
    date_updated = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'active', 'variations', 'date_created', 'date_updated']

    def create(self, validated_data):
        if not validated_data.get('variations'):
            product = Product.objects.create(**validated_data)
            ProductVariation.objects.create(product=product, name='-', price=0.00, active=False)
        else:
            variations_data = validated_data.pop('variations')
            product = Product.objects.create(**validated_data)
            for variation_data in variations_data:
                ProductVariation.objects.create(product=product, **variation_data)
        return product