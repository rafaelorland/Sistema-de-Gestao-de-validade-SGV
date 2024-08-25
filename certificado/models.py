from django.db import models

from instrumento.models import Instrumento

class Certificado(models.Model):
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    numero_certificado = models.CharField(max_length=255)
    data_validade = models.DateField()

    def __str__(self):
        return f"{self.numero_certificado} -  {self.data_validade} - {self.instrumento.veiculo.cliente.nome}"