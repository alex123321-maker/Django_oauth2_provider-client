"""
URL configuration for client_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from client_app import views
from django.conf import settings



# Настройте представления Swagger
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from drf_yasg.views import get_schema_view


SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title="API Title",
        default_version='v1',
        description="API description",
        # Дополнительные метаданные
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[OAuth2Authentication] 
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/login/', views.oauth2_login, name='oauth2_login'),
    path('oauth2/callback/', views.oauth2_callback, name='oauth2_callback'),
    path('login/', views.login, name='login'),
    path("api/" , include("client_app.urls")),
    path('swagger/', SCHEMA_VIEW.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SCHEMA_VIEW.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
