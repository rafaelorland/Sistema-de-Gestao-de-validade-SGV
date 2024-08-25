from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from .tasks import criar_notificacoes_para_certificados, verificar_e_enviar_notificacoes

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    criar_notificacoes_para_certificados()

    scheduler.add_job(
        criar_notificacoes_para_certificados,
        'interval',
        days=1,
        name='criar_notificacoes_periodicamente',
        jobstore='default'
    )

    scheduler.add_job(
        verificar_e_enviar_notificacoes,
        'cron',
        hour=10,
        minute=45,
        name='verificar_e_enviar_notificacoes',
        jobstore='default'
    )

    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
