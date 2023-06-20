from django.urls import path
from .views import MenuView

urlpatterns = [
    path('menu/', MenuView.as_view(), name='menu'),
]
