from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ProductVariation, Order, OrderItem
from .serializers import ProductVariationSerializer


class ProductVariationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer


# class OrderCreateView(generics.CreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(customer=self.request.user.customer)


# class OrderDetailView(generics.RetrieveAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]