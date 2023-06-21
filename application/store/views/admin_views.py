from rest_framework import generics
from ..models import Product
from rest_framework.permissions import IsAdminUser
from ..serializers.admin_serializers import ProductSerializer, UpdateProductSerializer


class AdminCreateProductView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AdminUpdateProductView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = UpdateProductSerializer
