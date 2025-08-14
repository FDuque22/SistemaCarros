from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages  # Para mostrar mensagens de erro
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Registro realizado com sucesso!")
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

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
    return redirect('cars_list')  # Redirecionar para a lista de carros

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