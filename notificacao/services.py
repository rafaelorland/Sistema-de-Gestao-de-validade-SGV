from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from .models import Notificacao
from certificado.models import Certificado

class NotificacaoService:
    def __init__(self, certificado):
        self.certificado = certificado

    def criar_notificacao(self, canal, mensagem, data_envio):
        """
        Cria uma notificação para o cliente relacionado ao certificado.
        """
        notificacao = Notificacao.objects.create(
            certificado=self.certificado,
            canal=canal,
            mensagem=mensagem,
            status='pendente',
            data_envio=data_envio
        )
        return notificacao

    def enviar_notificacao(self, notificacao):
        """
        Envia a notificação via o canal especificado.
        """
        if notificacao.canal == 'sms':
            self.enviar_sms(notificacao)
        elif notificacao.canal == 'email':
            self.enviar_email(notificacao)
        elif notificacao.canal == 'whatsapp':
            self.enviar_whatsapp(notificacao)
        
        notificacao.status = 'enviada'
        notificacao.data_envio = timezone.now().date()  # Atualiza a data de envio
        notificacao.save()

    def enviar_sms(self, notificacao):
        """
        Envia a notificação via SMS.
        """
        print(f"Enviando SMS para {notificacao.certificado.instrumento.veiculo.cliente}: {notificacao.mensagem}")

    def enviar_email(self, notificacao):
        """
        Envia a notificação via Email.
        """
        send_mail(
            subject='Notificação de Validade de Certificado',
            message=notificacao.mensagem,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[notificacao.certificado.instrumento.veiculo.cliente.email],
            fail_silently=False,
        )
        print(f"Enviando Email para {notificacao.certificado.instrumento.veiculo.cliente.email}: {notificacao.mensagem}")

    def enviar_whatsapp(self, notificacao):
        """
        Envia a notificação via WhatsApp.
        """
        print(f"Enviando WhatsApp para {notificacao.certificado.instrumento.veiculo.cliente}: {notificacao.mensagem}")

    def verificar_e_criar_notificacoes(self):
        """
        Verifica se existem notificações para o certificado e cria notificações se não houver.
        """
        hoje = timezone.now().date()
        periodos = [30, 15, 5]
        
        mensagens = {
            'email': lambda dias: f"Seu certificado ({self.certificado.numero_certificado}) expira em {dias} dias. Por favor, tome as devidas providências.",
            'sms': lambda dias: f"Certificado {self.certificado.numero_certificado} expira em {dias} dias.",
            'whatsapp': lambda dias: f"Certificado {self.certificado.numero_certificado} expira em {dias} dias. Verifique!"
        }

        with transaction.atomic():
            for dias in periodos:
                data_alvo = hoje + timedelta(days=dias)
                
                for canal, mensagem_func in mensagens.items():
                    # Verifica se já existe uma notificação para o mesmo canal e data de envio
                    if not Notificacao.objects.filter(
                        certificado=self.certificado,
                        canal=canal,
                        data_envio=data_alvo
                    ).exists():
                        mensagem = mensagem_func(dias)
                        self.criar_notificacao(
                            canal=canal,
                            mensagem=mensagem,
                            data_envio=data_alvo
                        )

    def enviar_notificacoes_pendentes(self):
        """
        Envia todas as notificações pendentes que estão programadas para hoje.
        """
        hoje = timezone.now().date()
        notificacoes_pendentes = Notificacao.objects.filter(
            status='pendente',
            data_envio=hoje
        )
        
        for notificacao in notificacoes_pendentes:
            self.enviar_notificacao(notificacao)
