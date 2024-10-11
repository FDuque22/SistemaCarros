from django.shortcuts import render, redirect
from cars.models import Car, Brand
from cars.forms import CarModelForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.conf import settings



class CarsView(View):
   
    def get(self, request):
        cars = Car.objects.filter(active=True).order_by('brand__name')
        search = request.GET.get('search')  # Verifica se mandou busca, se não, mostra todos

        if search:
            cars_by_model = Car.objects.filter(model__icontains=search, active=True)
            cars_by_brand = Car.objects.filter(brand__name__icontains=search, active=True)
            # Combine os dois QuerySets
            cars = cars_by_model | cars_by_brand
        
        return render(
            request, 
            'cars.html', 
            {'cars': cars}
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
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_delete.html'
    success_url = '/cars/'


    def post(self, request, *args, **kwargs):
        car = self.get_object()
        car.active = False  # Marque o carro como inativo
        car.save()
        return redirect(self.success_url)

    def get_object(self):
        # Obter o carro que será marcado como inativo
        return Car.objects.get(pk=self.kwargs['pk'])
    
def car_interest(request, pk):
    car = Car.objects.get(pk=pk)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Enviar e-mail para o superusuário
        send_mail(
            'Novo Interesse em um Carro',
            f'Nome: {name}\nE-mail: {email}\nTelefone: {phone}\n\nInteressado no carro: {car.brand} {car.model}',
            settings.DEFAULT_FROM_EMAIL,
            ['fjmultimarcassite@outlook.com'],
            fail_silently=False,
        )

        return redirect('success_page')  # Redirecione para uma página de sucesso ou de volta para os detalhes do carro

    return render(request, 'car_interest.html', {'car': car})