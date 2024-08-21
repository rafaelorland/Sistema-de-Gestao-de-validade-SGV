from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Notificacao
from django.db.models import Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

@login_required
def painel_notificacao(request):
    
    return render(request, 'painel_notificacao.html')

@login_required
def gerar_pdf_notificacoes(request):
    periodos = [7, 15, 30, 60, 90]
    status_choices = Notificacao.CERTIFICADO_STATUS_CHOICES
    canal_choices = ['email', 'sms', 'whatsapp']

    periodo_selecionado = int(request.GET.get('periodo', 30))
    status_selecionado = request.GET.get('status', '')
    canal_selecionado = request.GET.get('canal', '')
    cliente_nome = request.GET.get('cliente_nome', '')
    ordenacao = request.GET.get('ordenacao', '-data_envio_notificacao__data_envio')

    notificacoes = Notificacao.objects.filter(
        data_envio_notificacao__data_envio__gte=timezone.now() - timezone.timedelta(days=periodo_selecionado)
    )

    if status_selecionado:
        notificacoes = notificacoes.filter(status=status_selecionado)
    
    if canal_selecionado:
        notificacoes = notificacoes.filter(canal=canal_selecionado)
    
    if cliente_nome:
        notificacoes = notificacoes.filter(
            Q(certificado__instrumento__veiculo__cliente__nome__icontains=cliente_nome) |
            Q(certificado__numero_certificado__icontains=cliente_nome)
        )

    notificacoes = notificacoes.order_by(ordenacao)

    # Configurações do ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_notificacoes.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title = Paragraph("Relatório de Notificações", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Tabela de notificações
    data = [["Certificado", "Cliente", "Canal", "Data de Envio", "Status"]]
    
    for notificacao in notificacoes:
        status_display = notificacao.get_status_display()
        canal_display = notificacao.get_canal_display()
        data.append([
            notificacao.certificado.numero_certificado,
            notificacao.certificado.instrumento.veiculo.cliente.nome[:23],
            canal_display,
            notificacao.data_envio_notificacao.data_envio.strftime("%d/%m/%Y"),
            status_display,
        ])

    # Define a largura das colunas e ajusta o estilo de texto
    colWidths = [60, 150, 100, 100, 100]  # Ajuste as larguras conforme necessário
    table = Table(data, colWidths=colWidths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 1), (-1, -1), 'CJK'),  # Ajusta o texto para não exceder a largura da célula
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinha verticalmente o texto
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Ajuste a fonte para o corpo da tabela
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Ajuste o tamanho da fonte se necessário
        ('LEFTPADDING', (0, 1), (-1, -1), 5),  # Ajuste o padding para não cortar o texto
        ('RIGHTPADDING', (0, 1), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]))
    elements.append(table)

    # Construir o PDF
    doc.build(elements)
    return response

@login_required
def relatorio_notificacoes(request):
    # Filtros de período e status
    periodos = [7, 15, 30, 60, 90]
    status_choices = Notificacao.CERTIFICADO_STATUS_CHOICES
    canal_choices = ['email', 'sms', 'whatsapp']

    # Captura de parâmetros de filtro
    periodo_selecionado = int(request.GET.get('periodo', 30))
    status_selecionado = request.GET.get('status', '')
    canal_selecionado = request.GET.get('canal', '')
    cliente_nome = request.GET.get('cliente_nome', '')
    ordenacao = request.GET.get('ordenacao', '-data_envio_notificacao__data_envio')

    # Filtro de notificações
    notificacoes = Notificacao.objects.filter(
        data_envio_notificacao__data_envio__gte=timezone.now() - timezone.timedelta(days=periodo_selecionado)
    )

    if status_selecionado:
        notificacoes = notificacoes.filter(status=status_selecionado)
    
    if canal_selecionado:
        notificacoes = notificacoes.filter(canal=canal_selecionado)
    
    if cliente_nome:
        notificacoes = notificacoes.filter(
            Q(certificado__instrumento__veiculo__cliente__nome__icontains=cliente_nome) |
            Q(certificado__numero_certificado__icontains=cliente_nome)
        )

    # Ordenação
    notificacoes = notificacoes.order_by(ordenacao)

    # Paginação
    paginator = Paginator(notificacoes, 10)  # 10 notificações por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'periodos': periodos,
        'status_choices': status_choices,
        'canal_choices': canal_choices,  # Incluindo os canais no contexto
        'periodo_selecionado': periodo_selecionado,
        'status_selecionado': status_selecionado,
        'canal_selecionado': canal_selecionado,
        'cliente_nome': cliente_nome,
        'ordenacao': ordenacao,
        'notificacoes': page_obj,
        'page_obj': page_obj,
    }

    return render(request, 'relatorio_notificacoes.html', context)