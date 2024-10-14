from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from cars.forms import CarModelForm, InterestForm 
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
        car.active = False 
        car.save()
        return redirect(self.success_url)

    def get_object(self):
        return get_object_or_404(Car, pk=self.kwargs['pk'])

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