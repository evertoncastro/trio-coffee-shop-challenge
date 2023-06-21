from rest_framework import serializers
from .models import Product, ProductVariation, Order, OrderItem


class MenuVariationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'name', 'price']

class MenuModelSerializer(serializers.ModelSerializer):
    variations = MenuVariationModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'variations']


class OrderItemSerializer(serializers.Serializer):
    product_variation_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(10, 2, read_only=True)
    item_id = serializers.IntegerField(read_only=True)


class CreateOrderSerializer(serializers.Serializer):
    location = serializers.ChoiceField(choices=Order.LOCATION_CHOICES)
    order_items = OrderItemSerializer(many=True)


class OrderDetailModelSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'location', 'status', 'date_created', 'date_updated', 'order_items', 'total_price']

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        return OrderItemSerializer(order_items, many=True).data

    def get_total_price(self, obj):
        order_items = obj.order_items.all()
        total_price = sum(item.price * item.quantity for item in order_items)
        return total_price


class CreateOrderItemModelSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    item_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['quantity', 'item_id']

    def validate(self, attrs):
        order_id = self.context.get('view').kwargs.get('order_id')
        item_id = attrs['item_id']

        order_item_exists = OrderItem.objects.filter(order_id=order_id, item_id=item_id).exists()
        if order_item_exists:
            raise serializers.ValidationError(f"OrderItem with item_id {item_id} already exists in the order.")
        return attrs
    
    def create(self, validated_data):
        item_id = validated_data['item_id']
        product_variation: ProductVariation = ProductVariation.objects.filter(id=item_id).first()
        if not product_variation:
            raise serializers.ValidationError(f"ProductVariation with id {item_id} does not exist.")
        ModelClass = self.Meta.model
        return ModelClass._default_manager.create(price=product_variation.price, **validated_data)
    

class UpdateOrderItemModelSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ['quantity']

    def validate(self, attrs):
        order_item = self.instance
        if not order_item:
            raise serializers.ValidationError("Order item does not exist.")
        return attrs