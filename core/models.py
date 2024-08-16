from django.db import models


class SystemConfig(models.Model):
    notification_email = models.EmailField(default='admin@example.com')
    notification_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return "Configurações Globais do Sistema"