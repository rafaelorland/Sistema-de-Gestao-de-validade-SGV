from django.urls import path
from .views import painel_veiculo, adicionar_veiculo, editar_veiculo

urlpatterns = [
    path('', painel_veiculo, name='painel_veiculo'),
    path('<int:id>', painel_veiculo, name='veiculo_id'),
    path('add/', adicionar_veiculo, name='adicionar_veiculo'),
    path('edit/<int:id>', editar_veiculo, name='editar_veiculo'),
]
