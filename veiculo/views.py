import re
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from cliente.models import Cliente
from veiculo.models import Veiculo
from instrumento.models import Instrumento
from certificado.models import Certificado
@login_required
def adicionar_veiculo(request):
    if request.method == "POST":
        cliente_id = request.POST.get('cliente')
        placa = request.POST.get('placa').upper().strip()
        modelo = request.POST.get('modelo').strip()
        ano_fabricacao = request.POST.get('ano_fabricacao')

        if not ano_fabricacao.isdigit() or len(ano_fabricacao) != 4:
            messages.error(request, 'Ano de fabricação deve ser um número de 4 dígitos.')
            return redirect('adicionar_veiculo')

        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado.')
            return redirect('adicionar_veiculo')

        if Veiculo.objects.filter(placa=placa).exists():
            messages.error(request, 'Veículo com esta placa já está cadastrado.')
            return redirect('adicionar_veiculo')

        Veiculo.objects.create(cliente=cliente, placa=placa, modelo=modelo, ano_fabricacao=ano_fabricacao)

        messages.success(request, 'Veículo adicionado com sucesso.')
        return redirect('painel_veiculo')
    

    clientes = Cliente.objects.all()

    context = {
        'titulo_page': 'Adicionar veículo - SGV',
        'clientes': clientes,
    }

    return render(request, 'adicionar_veiculo.html', context)

@login_required
def editar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id)

    if request.method == "POST":
        placa = request.POST.get('placa')
        modelo = request.POST.get('modelo')
        ano_fabricacao = request.POST.get('ano_fabricacao')

        veiculo.placa = placa
        veiculo.modelo = modelo
        veiculo.ano_fabricacao = ano_fabricacao
        veiculo.save()

        messages.success(request, 'Veículo atualizado com sucesso.')
        return redirect('painel_veiculo')

    context = {
        'titulo_page': f'Editar Veículo {veiculo.placa} - SGV',
        'veiculo': veiculo,
    }
    return render(request, 'editar_veiculo.html', context)

@login_required
def painel_veiculo(request, id=None):
    if id is not None:
        veiculo = get_object_or_404(Veiculo, id=id)
        instrumentos = Instrumento.objects.filter(veiculo=veiculo)
        certificados = Certificado.objects.filter(instrumento__in=instrumentos)

        context = {
            'titulo_page': 'Veículo - SGV',
            'veiculo': veiculo,
            'instrumentos': instrumentos,
            'certificados': certificados,
        }
        return render(request, 'visualizar_veiculo.html', context)

    # Filtro de consulta
    query = request.GET.get('query', '').strip()
    filter_by = request.GET.get('filter_by', '').strip()

    query_clean = re.sub(r'\D', '', query)

    if not query:
        results = Veiculo.objects.all()
    else:
        if filter_by == 'Por Placa':
            results = Veiculo.objects.filter(placa__icontains=query)
            if not results.exists():
                messages.info(request, 'Nenhum veículo encontrado com a placa fornecida.')
        elif filter_by == 'Por CPF ou CNPJ':
            
            results = Veiculo.objects.filter(cliente__cpf_cnpj__icontains=query_clean)
            if not results.exists():
                messages.info(request, 'Nenhum veículo encontrado com o CPF ou CNPJ fornecido.')
        elif filter_by == 'Por Nome Cliente':
            results = Veiculo.objects.filter(cliente__nome__icontains=query)
            if not results.exists():
                messages.info(request, 'Nenhum veículo encontrado com o nome fornecido.')
        elif filter_by == 'Por Modelo':
            results = Veiculo.objects.filter(modelo__icontains=query)
            if not results.exists():
                messages.info(request, 'Nenhum veículo encontrado com o modelo fornecido.')
        elif filter_by == 'Por ID':
            try:
                id_query = int(query)
                results = Veiculo.objects.filter(id=id_query)
                if not results.exists():
                    messages.info(request, 'Nenhum veículo encontrado com o ID fornecido.')
            except ValueError:
                results = Veiculo.objects.none()
                messages.error(request, 'ID inválido. Certifique-se de que o ID seja um número inteiro.')
        else:
            results = Veiculo.objects.all()
            
    if not results.exists():
                messages.info(request, 'Nenhum veículo encontrado.')

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'titulo_page': 'Painel Veículo - SGV',
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
    }

    return render(request, 'painel_veiculo.html', context)
