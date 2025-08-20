from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Para mostrar mensagens de erro
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile  
from datetime import datetime, timedelta

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        data_assinatura = request.POST.get("data_assinatura")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe!")
            return render(request, "register.html", request.POST)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe um usuário com este e-mail!")
            return render(request, "register.html", request.POST)

        # 🔹 Cria usuário já inativo por padrão
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False   # <<<<<<<<<< aqui está a chave
        )
        senha_padrao = "123456"
        user.set_password(senha_padrao)
        user.save()

        # Cria o perfil
        profile = Profile(user=user)

        if data_assinatura:
            data_assinatura = datetime.strptime(data_assinatura, "%Y-%m-%d").date()
            data_expiracao = data_assinatura + timedelta(days=30)
            profile.data_assinatura = data_assinatura
            profile.data_expiracao = data_expiracao

            # Se expiração ainda não passou, ativa
            if datetime.today().date() <= data_expiracao:
                user.is_active = True
                user.save()

        profile.save()

        messages.success(request, f"Usuário {username} criado com sucesso! Senha padrão: {senha_padrao}")
        return redirect("inicio")

    return render(request, "register.html")

def editaruser(request, user_id):
    # Pega o usuário ou 404
    user = get_object_or_404(User, id=user_id)
    
    # Tenta pegar o perfil, cria se não existir
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        data_assinatura = request.POST.get("data_assinatura")

        # Verifica se o username já existe em outro usuário
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Outro usuário já possui este nome de usuário!")
            return render(request, "edit_user.html", {"user_obj": user})

        # Verifica se o email já existe em outro usuário
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Outro usuário já possui este e-mail!")
            return render(request, "edit_user.html", {"user_obj": user})

        # Atualiza dados do usuário
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # Atualiza assinatura e expiração
        if data_assinatura:
            data_assinatura = datetime.strptime(data_assinatura, "%Y-%m-%d").date()
            data_expiracao = data_assinatura + timedelta(days=30)
            profile.data_assinatura = data_assinatura
            profile.data_expiracao = data_expiracao

            # Ativa ou desativa automaticamente
            user.is_active = datetime.today().date() <= data_expiracao
        else:
            profile.data_assinatura = None
            profile.data_expiracao = None
            user.is_active = False

        user.save()
        profile.save()

        messages.success(request, f"Usuário {user.username} atualizado com sucesso!")
        return redirect("configuracoes")  # ou para onde quiser redirecionar

    # GET → renderiza formulário com valores atuais
    return render(request, "editaruser.html", {"user_obj": user, "profile": profile})

def configuracoes(request):
    """View para a página de configurações que lista todos os usuários"""
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'configuracoes.html', {'usuarios': usuarios})

def check_username(request):
    username = request.GET.get('username', None)
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cars_list')  # Redirecionar após login
        else:
            messages.error(request, "Usuário ou senha inválidos!")
    
    login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso!")  # Mensagem de sucesso
    return redirect('inicio')  # Redirecionar para a lista de carros

@login_required
def meu_perfil(request):
    return render(request, 'perfil.html')  # Template para Meu Perfil

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('/login')  # Redireciona para Meu Perfil
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'alterar_senha.html', {'form': form})  # Template para Alterar Senha