"""
URL configuration for sgv project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from sgv.views import login_view, home, logout_view

urlpatterns = [
    path('adminSGV/', admin.site.urls),
    path('', home, name='home'),
    path('cliente/', include('cliente.urls')),
    path('veiculo/', include('veiculo.urls')),
    path('instrumento/', include('instrumento.urls')),
    path('certificado/', include('certificado.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:  # Somente servir arquivos de mídia no modo debug
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)