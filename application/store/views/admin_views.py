from rest_framework import generics
from ..models import Product, ProductVariation
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from ..mixins import MultipleFieldLookupMixin
from ..serializers.admin_serializers import ProductSerializer, UpdateProductSerializer


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