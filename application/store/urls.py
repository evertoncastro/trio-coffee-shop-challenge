from django.urls import path
from .views import MenuView, CreateOrderView, CreateOrderItemView, UpdateDeleteOrderItemView, OrderDetailView

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('order/', CreateOrderView.as_view(), name='order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/<int:order_id>/order-item/', CreateOrderItemView.as_view(), name='order-item-create'),
    path('order/<int:order_id>/order-item/<int:id>/', UpdateDeleteOrderItemView.as_view(), name='order-item-update-delete'),
]
