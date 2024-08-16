from notificacao.services import NotificacaoService
from cliente.models import Cliente
from certificado.models import Certificado

# Exemplo de uso:
cliente = Cliente.objects.get(id=1)  # Seleciona um cliente específico
certificado = Certificado.objects.get(id=1)  # Seleciona um certificado específico

notificacao_service = NotificacaoService(certificado, cliente)

# Cria a notificação
notificacao = notificacao_service.criar_notificacao(
    canal='email',
    mensagem='Seu certificado expira em breve, por favor tome as providências.'
)

# Envia a notificação
notificacao_service.enviar_notificacao(notificacao)
