from django.db import models
from django.utils import timezone
from certificado.models import Certificado
from cliente.models import Cliente

class Notificacao(models.Model):
    CANAIS_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]

    certificado = models.ForeignKey(Certificado, on_delete=models.CASCADE)
    canal = models.CharField(max_length=10, choices=CANAIS_CHOICES)
    data_envio = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, default='pendente')
    mensagem = models.TextField()

    def __str__(self):
        return f"Notificação para {self.certificado.instrumento.veiculo.cliente.nome} via {self.canal}"
