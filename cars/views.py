from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from cars.forms import CarModelForm, InterestForm, ContatoForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from urllib.parse import quote
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q

@method_decorator(login_required(login_url='login'), name='dispatch')
# Classe para a visualização de carros
class CarsView(View):
    def get(self, request):
        cars = Car.objects.all().order_by('-data_criacao')

        search = request.GET.get('search', '').strip()
        tipo = request.GET.get('tipo', '').strip()  # para filtro por tipo separado

        if search:
            cars = cars.filter(
                Q(marca__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(model__icontains=search)
            )

        if tipo:
            cars = cars.filter(tipo__iexact=tipo)

        return render(
            request,
            'cars.html',
            {
                'cars': cars,
                'search': search,
                'tipo': tipo
            }
        )

@method_decorator(login_required(login_url='login'), name='dispatch')
# Classe para detalhes de um carro
class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'

# Classe para criação de novos carros
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
    
# Classe para atualização de carros
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        """Verifica se o usuário logado é o dono do carro"""
        car = self.get_object()
        return self.request.user == car.seller

# Classe para deletar carros (marcando como inativo)
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        car.active = False 
        car.save()
        return redirect(self.success_url)

    def get_object(self):
        return get_object_or_404(Car, pk=self.kwargs['pk'])

# Classe para o formulário de interesse em um carro
@method_decorator(login_required(login_url='login'), name='dispatch')
class InterestFormView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        form = InterestForm()
        return render(request, 'car_interest.html', {'form': form, 'car': car})

    def post(self, request, pk):
        car = get_object_or_404(Car, id=pk)
        form = InterestForm(request.POST)
        
        if form.is_valid():
            interest = form.save(commit=False)
            interest.car = car
            interest.save()

            owner_number = car.contact or ''
            owner_number = ''.join(filter(str.isdigit, owner_number))
            if owner_number.startswith('0'):
                owner_number = owner_number[1:]
            if not owner_number.startswith('55'):
                owner_number = '55' + owner_number

            message = (
                f"Olá, me chamo {interest.nome} e tenho interesse no {car.marca } { car.model} { car.color } { car.factory_year }/{ car.model_year }!\n\n"
            )

            whatsapp_url = f"https://wa.me/{owner_number}?text={quote(message)}"
            return JsonResponse({'whatsapp_url': whatsapp_url})

        return render(request, 'car_interest.html', {'form': form, 'car': car})

# Classe para o contato
@method_decorator(login_required(login_url='login'), name='dispatch')
class ContatoView(View):
    def get(self, request):
        form = ContatoForm()
        return render(request, 'contato.html', {'form': form})

    def post(self, request):
        form = ContatoForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua mensagem foi enviada com sucesso!')
            return redirect('contato_geral') 

        messages.error(request, 'Por favor, corrija os erros abaixo.')
        return render(request, 'contato.html', {'form': form})
    
# Classe para Planos
def plano(request):
    return render(request, "plano.html")

def inicio(request):
    if request.user.is_authenticated:
        return redirect('cars_list')  # precisa ser o name da URL correto
    return render(request, "inicio.html")

@login_required
def meus_anuncios(request):
    # Pega todos os carros cadastrados pelo usuário logado
    carros = Car.objects.filter(usuario=request.user).order_by('-data_criacao')
    quantidade = carros.count()

    return render(request, 'meus_anuncios.html', {
        'carros': carros,
        'quantidade': quantidade
    })