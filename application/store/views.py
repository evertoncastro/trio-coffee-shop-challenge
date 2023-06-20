from rest_framework import generics
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductVariation
from .serializers import MenuSerializer


class MenuView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Product.objects.filter(active=True).prefetch_related(
            Prefetch('variations', queryset=ProductVariation.objects.filter(active=True))
        )