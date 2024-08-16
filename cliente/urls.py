from django.urls import path
from .views import painel_cliente, adicionar_cliente, editar_cliente, buscar_cliente

urlpatterns = [
    path('', painel_cliente, name='painel_cliente'),
    path('<int:id>/', painel_cliente, name='cliente_id'),
    path('add/', adicionar_cliente, name='adicionar_cliente'),
    path('edit/<int:id>/', editar_cliente, name='editar_cliente'),
    path('buscar_cliente/', buscar_cliente, name='buscar_cliente'),
]
