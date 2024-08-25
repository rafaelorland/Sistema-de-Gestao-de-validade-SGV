from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from sgv import settings
from .models import Certificado, Notificacao, DataDeEnvioNotificacao
import logging

logger = logging.getLogger(__name__)

def criar_notificacoes_para_certificados():
    periodos = [30, 15, 5]  # Períodos para notificação, ajustar conforme necessário
    hoje = timezone.now().date()
    
    certificados = Certificado.objects.all()
    
    # for certificado in certificados:
    #     for dias in periodos:
    #         data_envio = certificado.data_validade - timedelta(days=dias)
            
    #         data_envio_notificacao, _ = DataDeEnvioNotificacao.objects.get_or_create(
    #             titulo=f"Notificação de {dias} dias",
    #             data_envio=data_envio
    #         )
            
    #         # Cria notificações se não existirem para esse período
    #         canais = ['email', 'sms', 'whatsapp']
    #         for canal in canais:
    #             if not Notificacao.objects.filter(
    #                 certificado=certificado,
    #                 canal=canal,
    #                 data_envio_notificacao=data_envio_notificacao
    #             ).exists():
    #                 mensagem = None
    #                 if canal == 'email':
    #                     mensagem = gerar_mensagem_email(certificado, dias)
    #                 elif canal == 'sms':
    #                     mensagem = gerar_mensagem_sms(certificado, dias)
    #                 elif canal == 'whatsapp':
    #                     mensagem = gerar_mensagem_whatsapp(certificado, dias)
                    
    #                 Notificacao.objects.create(
    #                     certificado=certificado,
    #                     canal=canal,
    #                     data_envio_notificacao=data_envio_notificacao,
    #                     mensagem=mensagem,
    #                     status='pendente'
    #                 )

def gerar_mensagem_email(certificado, dias):
    cliente = certificado.instrumento.veiculo.cliente
    instrumento = certificado.instrumento
    veiculo = instrumento.veiculo
    
    return (
        f"Prezado(a) {cliente.nome},\n\n"
        f"Estamos entrando em contato para informá-lo(a) que o seu Certificado de Verificação Subsequente do Cronotacógrafo "
        f"para o instrumento **{instrumento.tipo_instrumento.nome}** associado ao veículo **{veiculo.modelo}** "
        f"está se aproximando da data de validade.\n\n"
        f"**Data de Validade do Certificado:** {certificado.data_validade.strftime('%d/%m/%Y')}\n"
        f"**Faltam {dias} dias** para o vencimento do certificado.\n\n"
        f"Para consultas e mais informações, você pode utilizar o site oficial [https://cronotacografo.rbmlq.gov.br/](https://cronotacografo.rbmlq.gov.br/) "
        f"ou o aplicativo CertCrono, disponível na Google Play Store para Android.\n\n"
        f"Atenciosamente,\n\n"
        f"Equipe Lev LEV TRUCK’S CENTER"
    )

def gerar_mensagem_sms(certificado, dias):
    cliente = certificado.instrumento.veiculo.cliente
    instrumento = certificado.instrumento
    veiculo = instrumento.veiculo
    
    return (
        f"Olá {cliente.nome} cliente da LEV TRUCK’S CENTER, o Certificado de Verificação Subsequente do Cronotacógrafo "
        f"para o instrumento {instrumento.tipo_instrumento.nome} associado ao veículo {veiculo.modelo} "
        f"vence em {dias} dias. A data de validade é {certificado.data_validade.strftime('%d/%m/%Y')}. "
        f"Consulte mais informações no site [https://cronotacografo.rbmlq.gov.br/](https://cronotacografo.rbmlq.gov.br/) "
        f"ou no app CertCrono."
    )

def gerar_mensagem_whatsapp(certificado, dias):
    cliente = certificado.instrumento.veiculo.cliente
    instrumento = certificado.instrumento
    veiculo = instrumento.veiculo
    
    return (
        f"Olá {cliente.nome} cliente da LEV TRUCK’S CENTER,\n\n"
        f"Seu Certificado de Verificação Subsequente do Cronotacógrafo para o instrumento **{instrumento.tipo_instrumento.nome}** "
        f"associado ao veículo **{veiculo.modelo}** está prestes a vencer.\n\n"
        f"**Data de Validade:** {certificado.data_validade.strftime('%d/%m/%Y')}\n"
        f"**Faltam apenas {dias} dias** para o vencimento do certificado.\n\n"
        f"Para mais informações, acesse o site [https://cronotacografo.rbmlq.gov.br/](https://cronotacografo.rbmlq.gov.br/) "
        f"ou utilize o aplicativo CertCrono disponível na Google Play Store para Android.\n\n"
        f"Atenciosamente,\n\n"
        f"Equipe LEV TRUCK’S CENTER"
    )

def verificar_e_enviar_notificacoes():
    hoje = timezone.now().date()
    
    # Verifica notificações pendentes
    notificacoes_pendentes = Notificacao.objects.filter(
        data_envio_notificacao__data_envio=hoje,
        status='pendente'
    )
    
    for notificacao in notificacoes_pendentes:
        certificado = notificacao.certificado
        cliente = certificado.instrumento.veiculo.cliente
        
        try:
            if notificacao.canal == 'email':
                send_mail(
                    subject=f"Notificação de expiração - {certificado.numero_certificado}",
                    message=notificacao.mensagem,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[cliente.email]
                )
                notificacao.status = 'enviado'
                logger.info(f"Notificação por e-mail enviada para {cliente.email}.")
            
            elif notificacao.canal == 'sms':
                # Simular o envio de SMS
                # sms_id = enviar_sms(telefone.numero, mensagem_sms_curta)
                notificacao.status = 'enviado'
                logger.info(f"Notificação SMS enviada para {cliente.nome}.")
            
            elif notificacao.canal == 'whatsapp':
                # Simular o envio de WhatsApp
                # enviar_whatsapp(telefone.numero, mensagem_whatsapp)
                notificacao.status = 'enviado'
                logger.info(f"Notificação WhatsApp enviada para {cliente.nome}.")
        
        except Exception as e:
            notificacao.status = 'erro'
            logger.error(f"Erro ao enviar notificação {notificacao.canal} para {cliente.nome}: {e}")
        
        notificacao.save()
