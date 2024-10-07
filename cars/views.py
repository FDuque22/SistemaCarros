from django.shortcuts import render, redirect
from cars.models import Car, Brand
from cars.forms import CarModelForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

class CarsView(View):
   
   def get(self, request):
        cars = Car.objects.filter(active=True).order_by('brand__name')
        search = request.GET.get('search') #Verifica se mandou busca, se não, mostra todos

        if search:
            cars = Car.objects.filter(model__icontains=search) #Se houve busca, mande o filtro
        return render(
            request, 
            'cars.html', 
            {'cars': cars }
        )
   
class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
   
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required(login_url='login'), name='dispatch')
class CarDeleteView(View):
    model = Car
    template_name = 'car_delete.html'
    success_url = reverse_lazy('cars')

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        car.active = False  # Marque o carro como inativo
        car.save()
        return redirect(self.success_url)

    def get_object(self):
        # Obter o carro que será marcado como inativo
        return Car.objects.get(pk=self.kwargs['pk'])
