from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from certificado.models import Certificado
from instrumento.models import Instrumento
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

@login_required
def adicionar_certificado(request):
    if request.method == 'POST':
        numero_certificado = request.POST.get('numero_certificado')
        data_validade = request.POST.get('data_validade')
        instrumento_id = request.POST.get('instrumento')

        # Validação de campos obrigatórios
        if not numero_certificado or not data_validade or not instrumento_id:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'adicionar_certificado.html', {
                'instrumentos': Instrumento.objects.all(),
                'numero_certificado': numero_certificado,
                'data_validade': data_validade,
                'instrumento_id': instrumento_id
            })

        try:
            instrumento = Instrumento.objects.get(id=instrumento_id)
        except Instrumento.DoesNotExist:
            messages.error(request, 'Instrumento não encontrado.')
            return render(request, 'adicionar_certificado.html', {'instrumentos': Instrumento.objects.all()})

        # Verificar se o instrumento já possui um certificado
        if Certificado.objects.filter(instrumento=instrumento).exists():
            messages.error(request, 'Este instrumento já possui um certificado.')
            return render(request, 'adicionar_certificado.html', {
                'instrumentos': Instrumento.objects.all(),
                'numero_certificado': numero_certificado,
                'data_validade': data_validade,
                'instrumento_id': instrumento_id
            })

        try:
            certificado = Certificado(
                instrumento=instrumento,
                numero_certificado=numero_certificado,
                data_validade=data_validade
            )
            certificado.save()
            messages.success(request, 'Certificado adicionado com sucesso.')
            return redirect('painel_certificado')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao adicionar o certificado: {str(e)}')
            return render(request, 'adicionar_certificado.html', {
                'instrumentos': Instrumento.objects.all(),
                'numero_certificado': numero_certificado,
                'data_validade': data_validade,
                'instrumento_id': instrumento_id
            })

    else:
        instrumentos = Instrumento.objects.all()
        return render(request, 'adicionar_certificado.html', {'instrumentos': instrumentos})

@login_required
def editar_certificado(request, id):
    certificado = get_object_or_404(Certificado, id=id)

    if request.method == 'POST':
        numero_certificado = request.POST.get('numero_certificado')
        data_validade = request.POST.get('data_validade')
        instrumento_id = request.POST.get('instrumento')

        if not numero_certificado or not data_validade or not instrumento_id:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return render(request, 'editar_certificado.html', {
                'certificado': certificado,
                'instrumentos': Instrumento.objects.all(),
                'numero_certificado': numero_certificado,
                'data_validade': data_validade,
                'instrumento_id': instrumento_id
            })

        try:
            instrumento = Instrumento.objects.get(id=instrumento_id)
        except Instrumento.DoesNotExist:
            messages.error(request, 'Instrumento não encontrado.')
            return render(request, 'editar_certificado.html', {
                'certificado': certificado,
                'instrumentos': Instrumento.objects.all(),
                'numero_certificado': numero_certificado,
                'data_validade': data_validade,
                'instrumento_id': instrumento_id
            })

        try:
            certificado.instrumento = instrumento
            certificado.numero_certificado = numero_certificado
            certificado.data_validade = data_validade
            certificado.save()
            messages.success(request, 'Certificado atualizado com sucesso.')
            return redirect('painel_certificado')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao atualizar o certificado: {str(e)}')
            return render(request, 'editar_certificado.html', {
                'certificado': certificado,
                'instrumentos': Instrumento.objects.all(),
                'numero_certificado': numero_certificado,
                'data_validade': data_validade,
                'instrumento_id': instrumento_id
            })

    else:
        instrumentos = Instrumento.objects.all()
        data_validade_formato = certificado.data_validade.strftime('%Y-%m-%d') if certificado.data_validade else ''
        return render(request, 'editar_certificado.html', {
            'certificado': certificado,
            'instrumentos': instrumentos,
            'data_validade_formato': data_validade_formato
        })

@login_required
def painel_certificado(request, id=None):
    if id is not None:
        certificado = get_object_or_404(Certificado, id=id)
        contexto = {
            'titulo_page': 'Visualizar Certificado - SGV',
            'certificado': certificado,
        }
        return render(request, 'visualizar_certificado.html', contexto)

    # Listar certificados com filtros e paginação
    query = request.GET.get('query', '').strip()
    filter_by = request.GET.get('filter_by', '').strip()

    results = Certificado.objects.all()
    if query:
        if filter_by == 'Por Número':
            results = results.filter(numero_certificado__icontains=query)
        elif filter_by == 'Por Data de Validade':
            try:
                results = Certificado.objects.filter(data_validade=query)
            except ValueError:
                results = Certificado.objects.none()
                messages.error(request, 'Data inválida. Certifique-se de que a data esteja no formato correto.')
        elif filter_by == 'Por ID do Instrumento':
            try:
                id_query = int(query)
                results = Certificado.objects.filter(instrumento_id=id_query)
            except ValueError:
                results = Certificado.objects.none()
                messages.error(request, 'ID inválido. Certifique-se de que o ID seja um número inteiro.')
        else:
            results = Certificado.objects.none()
            messages.error(request, 'Filtro inválido.')

    if not results.exists():
        messages.info(request, 'Nenhum certificado encontrado.')

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    contexto = {
        'titulo_page': 'Painel Certificado - SGV',
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
    }

    return render(request, 'painel_certificado.html', contexto)
