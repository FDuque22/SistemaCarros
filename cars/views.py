from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from cars.forms import CarModelForm, InterestForm, ContatoForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages

# Classe para a visualização de carros
class CarsView(View):
    def get(self, request):
        category = request.GET.get('category')  # Obtém a categoria do parâmetro da URL
        cars = Car.objects.filter(active=True).order_by('brand__name')

        # Filtro de categoria
        if category == 'car':
            cars = cars.filter(category='car')
        elif category == 'moto':
            cars = cars.filter(category='moto')

        search = request.GET.get('search')
        if search:
            cars_by_model = cars.filter(model__icontains=search)
            cars_by_brand = cars.filter(brand__name__icontains=search)
            cars = cars_by_model | cars_by_brand

        return render(
            request, 
            'cars.html', 
            {'cars': cars}
        )
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

# Classe para atualização de carros
@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

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
            return redirect('car_detail', pk=pk)  

        return render(request, 'car_interest.html', {'form': form, 'car': car})

# Classe para o contato
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
