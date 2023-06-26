from django.urls import path
from .views.customer_views import (
    CreateUserView,
    MenuView,
    CreateOrderView,
    CreateOrderItemView,
    UpdateDeleteOrderItemView,
    ReadUpdateOrderView,
)
from .views.admin_views import (
    AdminCreateProductView,
    AdminUpdateProductView,
    AdminDeleteProductVariationView,
    AdminUpdateOrderStatusView,
)


urlpatterns = [
    path("user/", CreateUserView.as_view(), name="user-create"),
    path("menu/", MenuView.as_view(), name="menu"),
    path("orders/", CreateOrderView.as_view(), name="order"),
    path("orders/<int:pk>/", ReadUpdateOrderView.as_view(), name="order-read-update"),
    path(
        "orders/<int:order_id>/order-item/",
        CreateOrderItemView.as_view(),
        name="order-item-create",
    ),
    path(
        "orders/<int:order_id>/order-item/<int:id>/",
        UpdateDeleteOrderItemView.as_view(),
        name="order-item-update-delete",
    ),
    path(
        "admin/products", AdminCreateProductView.as_view(), name="admin-product-create"
    ),
    path(
        "admin/products/<int:pk>/",
        AdminUpdateProductView.as_view(),
        name="admin-product-update-delete",
    ),
    path(
        "admin/products/<int:product_id>/variations/<int:id>/",
        AdminDeleteProductVariationView.as_view(),
        name="admin-product-variation-delete",
    ),
    path(
        "admin/orders/<int:pk>/status/",
        AdminUpdateOrderStatusView.as_view(),
        name="admin-order-status-update",
    ),
]
