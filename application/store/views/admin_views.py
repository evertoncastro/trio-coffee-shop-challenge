from rest_framework import generics
from ..models import Product, ProductVariation, Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from ..mixins import MultipleFieldLookupMixin
from ..serializers.admin_serializers import (
    ProductSerializer, UpdateProductSerializer, UpdateOrderStatusSerializer
)
from django.core.mail import send_mail


class AdminCreateProductView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AdminUpdateProductView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = UpdateProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminDeleteProductVariationView(MultipleFieldLookupMixin, generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ProductVariation.objects.all()
    lookup_fields = ('product_id', 'id')

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AdminUpdateOrderStatusView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = UpdateOrderStatusSerializer

    def perform_update(self, serializer):
        instance: Order = serializer.save()
        # Send email to the customer user
        email_subject = f"Order Status Updated: Order #{instance.id}"
        email_message = f"Dear customer, your order with ID #{instance.id} has been updated to '{instance.status}'."
        data = send_mail(email_subject, email_message, 'from@example.com', [instance.customer.user.email])
        print(data)