from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView)


schema_view = get_schema_view(
    openapi.Info(
        title='Your API Title',
        default_version='v1',
        description='Your API description',
        contact=openapi.Contact(email='your_email@example.com'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('cofeeshop/api/', include("application.store.urls"), name='cofeeshop'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
