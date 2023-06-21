from .models import Order, OrderItem
from rest_framework.permissions import BasePermission

class IsOrderItemCustomer(BasePermission):
    def has_object_permission(self, request, view, obj: OrderItem):
        # Check if the authenticated user is the customer of the OrderItem
        return obj.order.customer.user == request.user
    

class IsOrderCustomer(BasePermission):
    def has_object_permission(self, request, view, obj: Order):
        # Check if the authenticated user is the customer of the Order
        return obj.customer.user == request.user

