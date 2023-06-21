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
    


class IsOrderItemOrderInWaitingStatus(BasePermission):
    message = 'The order cannot be modified when it is not in waiting status.'
    def has_object_permission(self, request, view, obj: OrderItem):
        # Check if order item order is in the waiting status
        return obj.order.status == Order.WAITING
    

class IsOrderInWaitingStatus(BasePermission):
    message = 'The order cannot be modified when it is not in waiting status.'
    def has_object_permission(self, request, view, obj: Order):
        # Check if order is in the waiting status
        return obj.status == Order.WAITING

