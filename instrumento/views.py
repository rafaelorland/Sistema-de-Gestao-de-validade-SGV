from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from certificado.models import Certificado
from cliente.models import Cliente
from instrumento.models import Instrumento, TipoInstrumento
from veiculo.models import Veiculo
import re

@login_required
def adicionar_instrumento(request):
    if request.method == "POST":
        veiculo_id = request.POST.get('veiculo')
        tipo_instrumento_id = request.POST.get('tipo_instrumento')
        numero_serie = request.POST.get('numero_serie')
        

        # Validação básica
        if not Veiculo.objects.filter(id=veiculo_id).exists():
            messages.error(request, 'Veículo inválido.')
            return redirect('adicionar_instrumento')
        
        if Instrumento.objects.filter(numero_serie=numero_serie).exists():
            messages.error(request, 'Número de série já cadastrado.')
            return redirect('adicionar_instrumento')

        # Criar o instrumento
        instrumento = Instrumento.objects.create(
            veiculo_id=veiculo_id,
            tipo_instrumento_id=tipo_instrumento_id,
            numero_serie=numero_serie,
        )
        
        messages.success(request, 'Instrumento adicionado com sucesso.')
        return redirect('painel_instrumento')

    veiculos = Veiculo.objects.all()
    tipos_instrumento = TipoInstrumento.objects.all()

    context = {
        'titulo_page': 'Adicionar Instrumento - SGV',
        'veiculos': veiculos,
        'tipos_instrumento': tipos_instrumento,
    }
    return render(request, 'adicionar_instrumento.html', context)

@login_required
def editar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    
    if request.method == 'POST':
        tipo_instrumento_id = request.POST.get('tipo_instrumento')
        numero_serie = request.POST.get('numero_serie')
        

        try:
            tipo_instrumento = TipoInstrumento.objects.get(id=tipo_instrumento_id)
        except TipoInstrumento.DoesNotExist:
            messages.error(request, 'Tipo de instrumento inválido.')
            return redirect('editar_instrumento', id=id)

        instrumento.tipo_instrumento = tipo_instrumento
        instrumento.numero_serie = numero_serie

        instrumento.save()

        messages.success(request, f'Instrumento ({numero_serie}) editado com sucesso.')
        return redirect('painel_instrumento')

    tipos_instrumento = TipoInstrumento.objects.all()

    context = {
        'titulo_page': f'Editar {instrumento.numero_serie} - SGV',
        'instrumento': instrumento,
        'tipos_instrumento': tipos_instrumento,
    }
    
    return render(request, 'editar_instrumento.html', context)

@login_required
def painel_instrumento(request, id=None):
    if id is not None:
        instrumento = get_object_or_404(Instrumento, id=id)
        veiculo = instrumento.veiculo
        tipo_instrumento = instrumento.tipo_instrumento

        certificados = Certificado.objects.filter(instrumento=instrumento)

        context = {
            'titulo_page': 'Instrumento - SGV',
            'instrumento': instrumento,
            'veiculo': veiculo,
            'tipo_instrumento': tipo_instrumento,
            'certificados': certificados
        }
        return render(request, 'visualizar_instrumento.html', context)

    query = request.GET.get('query', '').strip()
    filter_by = request.GET.get('filter_by', '').strip()

    results = Instrumento.objects.all()

    if query:
        if filter_by == 'Por Número de Série':
            results = results.filter(numero_serie__icontains=query)
        elif filter_by == 'Por Nome Cliente':
            results = results.filter(veiculo__cliente__nome__icontains=query)
        elif filter_by == 'Por Tipo de Instrumento':
            try:
                tipo = TipoInstrumento.objects.get(nome__icontains=query)
                results = results.filter(tipo_instrumento=tipo)
            except TipoInstrumento.DoesNotExist:
                results = Instrumento.objects.none()
                messages.error(request, 'Tipo de Instrumento não encontrado.')
        elif filter_by == 'Por Veículo':
            try:
                veiculo = Veiculo.objects.get(id=query)
                results = results.filter(veiculo=veiculo)
            except Veiculo.DoesNotExist:
                results = Instrumento.objects.none()
                messages.error(request, 'Veículo não encontrado.')
        elif filter_by == 'Por ID':
            try:
                id_query = int(query)
                results = results.filter(id=id_query)
            except ValueError:
                results = Instrumento.objects.none()
                messages.error(request, 'ID inválido. Certifique-se de que o ID seja um número inteiro.')

    if not results.exists():
        messages.info(request, 'Nenhum instrumento encontrado.')

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'titulo_page': 'Painel Instrumento - SGV',
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
    }

    return render(request, 'painel_instrumento.html', context)
