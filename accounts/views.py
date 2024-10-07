from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages  # Para mostrar mensagens de erro

def register_view(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Registro realizado com sucesso! Você pode fazer login.")
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
            return redirect('cars_list')  # Redirecionar para a lista de carros
        else:
            messages.error(request, "Usuário ou senha inválidos.")  # Mensagem de erro
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")  # Mensagem de sucesso
    return redirect('login')  # Redirecionar para a lista de carros
