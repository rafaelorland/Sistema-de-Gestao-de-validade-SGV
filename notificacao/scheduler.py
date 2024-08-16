from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
from django_apscheduler.jobstores import DjangoJobStore, register_events # type: ignore
from django.utils import timezone
from datetime import timedelta
from certificado.models import Certificado
from notificacao.models import Notificacao
from .services import NotificacaoService

def enviar_notificacoes():
    """
    Verifica e cria notificações para os certificados cujas datas de validade estão se aproximando.
    """
    hoje = timezone.now().date()
    periodos = [30, 15, 5]

    for dias in periodos:
        data_alvo = hoje + timedelta(days=dias)
        certificados = Certificado.objects.filter(data_validade=data_alvo)

        print(f'Aqui passou em Verificar diaa. Foram {certificados.count()} encontrados')

        for certificado in certificados:
            print(f"Processando certificado {certificado.numero_certificado} com validade em {certificado.data_validade}")
            notificacao_service = NotificacaoService(certificado)
            notificacao_service.verificar_e_criar_notificacoes()

def enviar_notificacoes_pendentes():
    """
    Envia todas as notificações pendentes que estão programadas para hoje.
    """
    hoje = timezone.now().date()
    notificacoes_pendentes = Notificacao.objects.filter(
        status='pendente',
        data_envio=hoje
    )
    
    for notificacao in notificacoes_pendentes:
        notificacao_service = NotificacaoService(notificacao.certificado)
        notificacao_service.enviar_notificacao(notificacao)

def start_scheduler():
    """
    Inicia o agendador para execução de tarefas periódicas.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Agendamento para verificar e criar notificações diariamente
    scheduler.add_job(
        enviar_notificacoes,
        'cron',
        hour=5,
        minute=49,
        name='enviar_notificacoes_diariamente',
        jobstore='default'
    )

    # Agendamento para enviar notificações pendentes diariamente
    scheduler.add_job(
        enviar_notificacoes_pendentes,
        'cron',
        hour=5,
        minute=49,
        name='enviar_notificacoes_pendentes_diariamente',
        jobstore='default'
    )

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
