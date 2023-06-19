from django.urls import path
from .views import ProductVariationListView

urlpatterns = [
    path('product-variations/', ProductVariationListView.as_view(), name='product-variation-list')
]
