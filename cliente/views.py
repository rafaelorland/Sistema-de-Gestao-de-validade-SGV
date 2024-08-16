from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from certificado.models import Certificado
from cliente.models import Cliente, TelefoneCliente
from instrumento.models import Instrumento
from veiculo.models import Veiculo
import re

@login_required
def buscar_cliente(request):
    query = request.GET.get('query', '')
    clientes = Cliente.objects.filter(nome__icontains=query)[:10]
    cliente_list = [{'id': cliente.id, 'nome': cliente.nome} for cliente in clientes]
    return JsonResponse(cliente_list, safe=False)

@login_required
def adicionar_cliente(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')

        cpf_cnpj_clean = re.sub(r'\D', '', cpf_cnpj)

        # Validação simples de CPF e CNPJ
        if len(cpf_cnpj_clean) not in [11, 14]:
            messages.error(request, 'Número de CPF deve ter 11 dígitos ou número de CNPJ deve ter 14 dígitos.')
            return render(request, 'adicionar_cliente.html')

        
        cliente = Cliente.objects.create(nome=nome, cpf_cnpj=cpf_cnpj_clean, endereco=endereco, email=email)

        numeros = [re.sub(r'\D', '', numero) for numero in request.POST.getlist('numero[]')]

        for i in range(len(numeros)):
            numero = numeros[i]
            TelefoneCliente.objects.create(cliente=cliente, numero=numero)

        messages.success(request, 'Cliente adicionado com sucesso.')
        return redirect('painel_cliente')
    context = {
        'titulo_page': 'Adicionar cliente - SGV',
    }
    return render(request, 'adicionar_cliente.html', context)

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    telefones = TelefoneCliente.objects.filter(cliente=cliente)

    if request.method == "POST":
        nome = request.POST.get('nome')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')

        # Limpar caracteres não numéricos do CPF/CNPJ
        cpf_cnpj_clean = re.sub(r'\D', '', cpf_cnpj)

        # Validação simples de CPF e CNPJ
        if len(cpf_cnpj_clean) not in [11, 14]:
            messages.error(request, 'Número de CPF deve ter 11 dígitos ou número de CNPJ deve ter 14 dígitos.')
            return render(request, 'editar_cliente.html', {'cliente': cliente, 'telefones': telefones})

        
        # Atualizar cliente
        cliente.nome = nome
        cliente.cpf_cnpj = cpf_cnpj_clean
        cliente.endereco = endereco
        cliente.email = email
        cliente.save()

        # Atualizar telefones
        numeros = [re.sub(r'\D', '', numero) for numero in request.POST.getlist('numero[]')]

        # Remover telefones existentes
        TelefoneCliente.objects.filter(cliente=cliente).delete()

        for i in range(len(numeros)):
            numero = numeros[i]
            TelefoneCliente.objects.create(cliente=cliente, numero=numero)

        messages.success(request, 'Cliente atualizado com sucesso.')
        return redirect('painel_cliente')

    context = {
        'titulo_page': f'Editar {cliente.nome} - SGV',
        'cliente': cliente,
        'telefones': telefones,
    }
    return render(request, 'editar_cliente.html', context)

@login_required
def painel_cliente(request, id=None):
    if id is not None:
        cliente = get_object_or_404(Cliente, id=id)
        telefones = TelefoneCliente.objects.filter(cliente=cliente)
        veiculos = Veiculo.objects.filter(cliente=cliente)
        instrumentos = Instrumento.objects.filter(veiculo__in=veiculos)
        certificados = Certificado.objects.filter(instrumento__in=instrumentos)

        context = {
            'titulo_page': 'Cliente - SGV',
            'cliente': cliente,
            'telefones': telefones,
            'veiculos': veiculos,
            'instrumentos': instrumentos,
            'certificados': certificados,
        }
        return render(request, 'visualizar_cliente.html', context)

    query = request.GET.get('query', '').strip()
    filter_by = request.GET.get('filter_by', '').strip()

    query_clean = re.sub(r'\D', '', query)

    if not query:
        results = Cliente.objects.all()
    else:
        if filter_by == 'Por Nome':
            results = Cliente.objects.filter(nome__icontains=query)
        elif filter_by == 'Por CPF ou CNPJ':
            if len(query_clean) in [11, 14]:
                results = Cliente.objects.filter(cpf_cnpj=query_clean)
            else:
                results = Cliente.objects.none()
                messages.error(request, 'Número de CPF/CNPJ inválido. Certifique-se de que tenha 11 dígitos (CPF) ou 14 dígitos (CNPJ).')
        elif filter_by == 'Por ID':
            try:
                id_query = int(query)
                results = Cliente.objects.filter(id=id_query)
            except ValueError:
                results = Cliente.objects.none()
                messages.error(request, 'ID inválido. Certifique-se de que o ID seja um número inteiro.')
        else:
            results = Cliente.objects.all()

        if not results.exists():
            messages.info(request, 'Nenhum cliente encontrado.')

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'titulo_page': 'Painel Cliente - SGV',
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
    }

    return render(request, 'painel_cliente.html', context)
