from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from cars.forms import CarModelForm, InterestForm  # Não esqueça de importar o InterestForm
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

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

# Nova view para processar o formulário de interesse
class InterestFormView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, pk=car_id)
        form = InterestForm()
        return render(request, 'interest_form.html', {'form': form, 'car': car})

    def post(self, request, car_id):
        form = InterestForm(request.POST)
        car = get_object_or_404(Car, pk=car_id)

        if form.is_valid():
            # Aqui você pode salvar os dados do formulário em um modelo que você criou para armazenar os interesses
            # Exemplo:
            # Interest.objects.create(car=car, **form.cleaned_data)

            # Redirecionar após o sucesso
            return redirect('success_page')  # Altere 'success_page' para a URL que você deseja redirecionar após o envio

        return render(request, 'interest_form.html', {'form': form, 'car': car})
