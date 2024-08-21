from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_notificacao, name='painel_notificacao'),
]
