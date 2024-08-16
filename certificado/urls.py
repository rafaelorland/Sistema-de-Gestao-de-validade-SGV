from django.urls import path
from .views import painel_certificado, adicionar_certificado, editar_certificado

urlpatterns = [
    path('', painel_certificado, name='painel_certificado'),
    path('<int:id>/', painel_certificado, name='certificado_id'),
    path('add/', adicionar_certificado, name='adicionar_certificado'),
    path('edit/<int:id>', editar_certificado, name='editar_certificado'),
]
