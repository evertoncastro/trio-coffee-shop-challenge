from rest_framework import serializers
from ..models import Product, ProductVariation, Order


class ProductVariationSerializer(serializers.ModelSerializer):
    date_created = serializers.CharField(read_only=True)
    date_updated = serializers.CharField(read_only=True)
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = ProductVariation
        fields = ["name", "price", "active", "date_created", "date_updated"]


class ProductSerializer(serializers.ModelSerializer):
    variations = ProductVariationSerializer(many=True, required=False)
    date_created = serializers.CharField(read_only=True)
    date_updated = serializers.CharField(read_only=True)
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "active", "variations", "date_created", "date_updated"]

    def create(self, validated_data):
        if not validated_data.get("variations"):
            product = Product.objects.create(**validated_data)
            ProductVariation.objects.create(
                product=product, name="-", price=0.00, active=False
            )
        else:
            variations_data = validated_data.pop("variations")
            product = Product.objects.create(**validated_data)
            for variation_data in variations_data:
                ProductVariation.objects.create(product=product, **variation_data)
        return product


class UpdateProductVariationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductVariation
        fields = ["id", "name", "price", "active"]


class UpdateProductSerializer(serializers.ModelSerializer):
    variations = UpdateProductVariationSerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "active", "variations"]

    def update(self, instance, validated_data):
        variations_data = validated_data.pop("variations", [])
        instance.name = validated_data.get("name", instance.name)
        instance.active = validated_data.get("active", instance.active)
        instance.save()

        # Update or create variations
        for variation_data in variations_data:
            variation_id = variation_data.get("id")
            if variation_id:
                try:
                    variation = ProductVariation.objects.get(
                        id=variation_id, product=instance
                    )
                    variation.name = variation_data.get("name", variation.name)
                    variation.price = variation_data.get("price", variation.price)
                    variation.active = variation_data.get("active", variation.active)
                    variation.save()
                except ProductVariation.DoesNotExist:
                    pass
            else:
                ProductVariation.objects.create(product=instance, **variation_data)

        return instance


class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
