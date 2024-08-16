from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from certificado.models import Certificado
from cliente.models import Cliente
from instrumento.models import Instrumento
from veiculo.models import Veiculo
from datetime import datetime, timedelta

@login_required
def home(request):
    # Estatísticas gerais
    total_clientes = Cliente.objects.count()
    total_veiculos = Veiculo.objects.count()
    total_instrumentos = Instrumento.objects.count()
    total_certificados = Certificado.objects.count()

    hoje = datetime.now().date()
    data_limite_1_mes = hoje + timedelta(days=30)
    data_limite_1_semana = hoje + timedelta(days=7)

    proximos_da_validade_1_mes = Certificado.objects.filter(
        data_validade__lte=data_limite_1_mes, data_validade__gte=hoje
    ).count()
    
    proximos_da_validade_1_semana = Certificado.objects.filter(
        data_validade__lte=data_limite_1_semana, data_validade__gte=hoje
    ).count()

    vencidos = Certificado.objects.filter(
        data_validade__lt=hoje
    ).count()
    
    context = {
        'titulo_page': 'Home - SGV',
        'total_clientes': total_clientes,
        'total_veiculos': total_veiculos,
        'total_instrumentos': total_instrumentos,
        'total_certificados': total_certificados,
        'proximos_da_validade_1_mes': proximos_da_validade_1_mes,
        'proximos_da_validade_1_semana': proximos_da_validade_1_semana,
        'vencidos': vencidos,
    }
    
    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            if username and password:
                messages.error(request, 'Usuário ou senha incorretos. Por favor, tente novamente.')
            elif not username:
                messages.error(request, 'O campo de usuário é obrigatório.')
            elif not password:
                messages.error(request, 'O campo de senha é obrigatório.')

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')
