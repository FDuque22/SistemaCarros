from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car, Interesse
from cars.forms import CarModelForm, InteresseForm
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
        return get_object_or_404(Car, pk=self.kwargs['pk'])


# View para capturar o interesse no carro
class TenhoInteresseView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        form = InteresseForm()
        return render(request, 'car_interest.html', {'form': form, 'car': car})

    def post(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        form = InteresseForm(request.POST)
        
        if form.is_valid():
            interesse = form.save(commit=False)
            interesse.carro = car
            interesse.save()

            # Opcional: enviar um e-mail notificando sobre o interesse
            send_mail(
                'Novo Interesse no Carro',
                f'Novo interesse de {interesse.nome} no carro {car.model}.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_TO_EMAIL],  # Troque pelo e-mail do destinatário
            )

            return redirect('sucesso_interesse')

        return render(request, 'car_interest.html', {'form': form, 'car': car})
