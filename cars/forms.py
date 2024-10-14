from django import forms
from cars.models import Car

#Criação do formulário para o usuário cadastrar carros para venda
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ("active",)
        fields = '__all__'

    #def clean_value(self):   #Validação do Campo sempre será clean_CAMPO
    #    value = self.cleaned_data.get('value')
    #   if value < 20000:
    #        self.add_error('value', 'Valor mínimo do carro deve ser de R$20.000,00')
    #    return value

    #def clean_factory_year(self):
    #    factory_year = self.cleaned_data.get('factory_year')
    #    if factory_year < 1975:
    #        self.add_error('factory_year', 'Ano mínimo: 1976')
    #    return factory_year

