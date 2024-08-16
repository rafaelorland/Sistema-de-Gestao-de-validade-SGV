from django.db import models

from cliente.models import Cliente

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='veiculos')
    placa = models.CharField(max_length=7, unique=True)
    modelo = models.CharField(max_length=255)
    ano_fabricacao = models.IntegerField()

    def __str__(self):
        return f"{self.placa} - {self.modelo}"