from django.urls import path
from .views import painel_instrumento, adicionar_instrumento, editar_instrumento

urlpatterns = [
    path('', painel_instrumento, name='painel_instrumento'),
    path('<int:id>/', painel_instrumento, name='instrumento_id'),
    path('add/', adicionar_instrumento, name='adicionar_instrumento'),
    path('edit/<int:id>', editar_instrumento, name='editar_instrumento'),
    
]
