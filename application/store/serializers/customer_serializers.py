from rest_framework import serializers
from ..models import Product, ProductVariation, Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
    id = serializers.IntegerField(read_only=True)
    product_variation_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(10, 2, read_only=True)
    name = serializers.CharField(read_only=True)
    item_id = serializers.IntegerField(read_only=True)


class CreateOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    location = serializers.ChoiceField(choices=Order.LOCATION_CHOICES)
    status = serializers.CharField(read_only=True)
    order_items = OrderItemSerializer(many=True)
    date_created = serializers.CharField(read_only=True)
    date_updated = serializers.CharField(read_only=True)


class ReadUpdateModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    order_items = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    date_created = serializers.CharField(read_only=True)
    date_updated = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'location', 'status', 'canceled', 'date_created', 'date_updated', 'order_items', 'total_price']

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        return OrderItemSerializer(order_items, many=True).data

    def get_total_price(self, obj):
        order_items = obj.order_items.all()
        total_price = sum(item.price * item.quantity for item in order_items)
        return total_price
    
    def validate(self, attrs):
        if self.instance.status == Order.DELIVERED and attrs.get('canceled') == True:
            raise serializers.ValidationError("Delivered order cannot be canceled")
        if self.instance.canceled and attrs.get('canceled') == False:
            raise serializers.ValidationError("Canceled order cannot be released")
        if self.instance.canceled:
            raise serializers.ValidationError("Canceled order cannot be updated")
        return attrs


class CreateOrderItemModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    item_id = serializers.IntegerField()
    price = serializers.DecimalField(10, 2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'item_id', 'price']

    def validate(self, attrs):
        order_id = self.context.get('view').kwargs.get('order_id')
        item_id = attrs['item_id']

        order_item_exists = OrderItem.objects.filter(order_id=order_id, item_id=item_id).exists()
        if order_item_exists:
            raise serializers.ValidationError(f"OrderItem with item_id {item_id} already exists in the order.")
        return attrs
    
    def create(self, validated_data):
        item_id = validated_data['item_id']
        variation: ProductVariation = ProductVariation.objects.filter(id=item_id).first()
        if not variation:
            raise serializers.ValidationError(f"ProductVariation with id {item_id} does not exist.")
        ModelClass = self.Meta.model
        name = f'{variation.product.name} ({variation.name})' if variation.name != '-' else variation.product.name
        return ModelClass._default_manager.create(
            price=variation.price, 
            name=name,
            **validated_data
        )
    

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