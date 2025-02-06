"""
URL configuration for project_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('solar-api/admin/', admin.site.urls),
    
    # FIX: Ensure correct schema URL
    path('solar-api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    
    # FIX: Ensure the Swagger UI references the correct schema
    path('solar-api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

    # Redirect default API path to documentation
    path('', RedirectView.as_view(url='/solar-api/docs/', permanent=False), name='index'),

    # Other API routes
    path('solar-api/user/', include('user.urls')),
    path('solar-api/core/', include('core.urls')),
]

