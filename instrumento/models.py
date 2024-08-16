from django.db import models

from veiculo.models import Veiculo

class TipoInstrumento(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome


class Instrumento(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='instrumentos')
    tipo_instrumento = models.ForeignKey(TipoInstrumento, on_delete=models.CASCADE, related_name='instrumentos')
    numero_serie = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.tipo_instrumento.nome} - {self.numero_serie}"