from django.urls import path
from .views.customer_views import (
    MenuView, 
    CreateOrderView, 
    CreateOrderItemView, 
    UpdateDeleteOrderItemView, 
    ReadUpdateOrderView
)
from .views.admin_views import AdminCreateProductView, AdminUpdateProductView


urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('order/', CreateOrderView.as_view(), name='order'),
    path('order/<int:pk>/', ReadUpdateOrderView.as_view(), name='order-read-update'),
    path('order/<int:order_id>/order-item/', CreateOrderItemView.as_view(), name='order-item-create'),
    path('order/<int:order_id>/order-item/<int:id>/', UpdateDeleteOrderItemView.as_view(), name='order-item-update-delete'),

    path('admin/product', AdminCreateProductView.as_view(), name='admin-product-create'),
    path('admin/product/<int:pk>/', AdminUpdateProductView.as_view(), name='admin-product-update'),
]
