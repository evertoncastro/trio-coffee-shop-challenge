from django.urls import path
from .views import MenuView, OrderCreateView

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
    path('order/', OrderCreateView.as_view(), name='order'),
]
