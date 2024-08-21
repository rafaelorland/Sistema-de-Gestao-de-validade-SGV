from django.contrib import admin

from notificacao.models import Notificacao, DataDeEnvioNotificacao

# Register your models here.
admin.site.register(Notificacao)
admin.site.register(DataDeEnvioNotificacao)