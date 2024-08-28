"""
URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from debug_toolbar.toolbar import debug_toolbar_urls

from root import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from root import custom_token
from texnomart import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('texnomart-uz/', include('texnomart.urls')),
                  path('api-auth/', include('rest_framework.urls')),
                  path('texnomart-uz/token-auth/', custom_token.CustomAuthToken.as_view()),
                  path('texnomart-uz/api/token/', TokenObtainPairView.as_view()),
                  path('texnomart-uz/api/token/refresh/', TokenRefreshView.as_view()),
                  path('api/token/blacklist/', TokenBlacklistView.as_view()),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += debug_toolbar_urls()

