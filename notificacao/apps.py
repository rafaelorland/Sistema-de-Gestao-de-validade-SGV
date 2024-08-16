from django.apps import AppConfig


class NotificacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notificacao'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()