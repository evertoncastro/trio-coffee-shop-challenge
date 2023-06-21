from django.urls import path
from .views import MenuView, CreateOrderView, CreateOrderItemView

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('order/', CreateOrderView.as_view(), name='order'),
    path('order/<int:order_id>/order-item/', CreateOrderItemView.as_view(), name='order-item-create'),
]
