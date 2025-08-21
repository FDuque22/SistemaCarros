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
from datetime import datetime, timedelta, date
from django.db.models import Q, F, ExpressionWrapper, IntegerField
from cars.models import Car

@login_required
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

        # 🔹 Cria usuário (inativo por padrão, exceto admins)
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )
        senha_padrao = "123456"
        user.set_password(senha_padrao)

        # Se for Felipe ou Bruno, sempre ativo
        if username.lower() in ["felipe", "bruno"]:
            user.is_active = True
            user.is_superuser = True
            user.is_staff = True

        user.save()

        # Cria o perfil
        profile = Profile(user=user)

        if data_assinatura:
            data_assinatura = datetime.strptime(data_assinatura, "%Y-%m-%d").date()
            data_expiracao = data_assinatura + timedelta(days=30)

            profile.data_assinatura = data_assinatura
            profile.data_expiracao = data_expiracao

            # Só faz checagem de dias se não for admin
            if username.lower() not in ["felipe", "bruno"]:
                dias_restantes = (data_expiracao - date.today()).days
                if dias_restantes >= 0:
                    user.is_active = True
                else:
                    user.is_active = False
                user.save()

        profile.save()

        messages.success(
            request,
            f"Usuário {username} criado com sucesso! Senha padrão: {senha_padrao}"
        )
        return redirect("inicio")

    return render(request, "register.html")


@login_required
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

@login_required
def configuracoes(request):
    """View para a página de configurações que lista todos os usuários"""
    search = request.GET.get("search")
    ordenar = request.GET.get("ordenar")  # "mais_dias" ou "menos_dias"

    usuarios = User.objects.all().order_by('-date_joined')

    # 🔍 Filtro de busca (username ou email)
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    # ⏳ Filtro de dias restantes (ordenação)
    if ordenar in ["mais_dias", "menos_dias"]:
        usuarios = usuarios.annotate(
            dias_restantes=ExpressionWrapper(
                F("profile__data_expiracao") - date.today(),
                output_field=IntegerField()
            )
        )
        if ordenar == "mais_dias":
            usuarios = usuarios.order_by(F("dias_restantes").desc(nulls_last=True))
        else:  # menos_dias
            usuarios = usuarios.order_by(F("dias_restantes").asc(nulls_last=True))

    return render(request, "configuracoes.html", {"usuarios": usuarios})

@login_required
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
    usuario = request.user
    dias_restantes = None

    if hasattr(usuario, 'profile') and usuario.profile.data_expiracao:
        dias_restantes = (usuario.profile.data_expiracao - date.today()).days
        if dias_restantes < 0:
            dias_restantes = 0

        # Admins sempre ativo, não mostra dias
        if usuario.username.lower() in ["felipe", "bruno"]:
            dias_restantes = None

    carros_cadastrados = Car.objects.filter(usuario=usuario).count()

    return render(request, 'perfil.html', {
        'usuario': usuario,
        'dias_restantes': dias_restantes,
        'carros_cadastrados': carros_cadastrados
    })

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