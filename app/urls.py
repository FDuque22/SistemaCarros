from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars.views import CarsView, NewCarCreateView, CarDetailView, CarUpdateView, CarDeleteView, InterestFormView, ContatoView
from accounts.views import register_view, login_view, logout_view, meu_perfil, alterar_senha  # Importando as views necessárias

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('accounts/', include('django.contrib.auth.urls')),  # Adiciona as URLs de autenticação do Django

    # Views de Carros
    path('cars/', CarsView.as_view(), name='cars_list'),
    path('', CarsView.as_view(), name='cars_list'),
    path('new_car/', NewCarCreateView.as_view(), name='new_car'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('car/<int:pk>/interest/', InterestFormView.as_view(), name='interest_form'),
    path('contato/', ContatoView.as_view(), name='contato_geral'),

    # URLs do app accounts
    path('meu_perfil/', meu_perfil, name='meu_perfil'),  # URL para Meu Perfil
    path('alterar_senha/', alterar_senha, name='alterar_senha'),  # URL para Alterar Senha

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
