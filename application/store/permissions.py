from .models import OrderItem
from rest_framework.permissions import BasePermission

class IsOrderItemCustomer(BasePermission):
    def has_object_permission(self, request, view, obj: OrderItem):
        # Check if the authenticated user is the customer of the OrderItem
        return obj.order.customer.user == request.user
