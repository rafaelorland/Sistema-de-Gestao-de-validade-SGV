from django.db import models

from certificado.models import Certificado

class Notificacao(models.Model):
    CERTIFICADO_STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('enviado', 'Enviado'),
        ('erro', 'Erro'),
    ]
    
    certificado = models.ForeignKey(Certificado, on_delete=models.CASCADE)
    canal = models.CharField(max_length=20, choices=[('email', 'E-mail'), ('sms', 'SMS'), ('whatsapp', 'WhatsApp')])
    data_envio_notificacao = models.ForeignKey('DataDeEnvioNotificacao', on_delete=models.CASCADE)
    mensagem = models.TextField()
    status = models.CharField(max_length=10, choices=CERTIFICADO_STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f'{self.certificado.numero_certificado} - {self.certificado.instrumento.numero_serie} - {self.certificado.instrumento.veiculo.placa} - {self.certificado.instrumento.veiculo.cliente.nome} - '

class DataDeEnvioNotificacao(models.Model):
    titulo = models.CharField(max_length=255)
    data_envio = models.DateField()

    def __str__(self):
        return f'{self.titulo} - {self.data_envio}'
