from rest_framework import generics
from ..models import Product
from ..serializers.admin_serializers import ProductSerializer


class AdminCreateProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
