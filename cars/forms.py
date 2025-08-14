from django import forms
from cars.models import Car, CarInterest, Contato

# Criação do formulário para o usuário cadastrar carros para venda
class CarModelForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ["usuario"]  # Não mostrar o campo de usuário
        widgets = {
            "marca": forms.Select(attrs={"class": "carnew-form-input"}),
            "model": forms.TextInput(attrs={"class": "carnew-form-input"}),
            "factory_year": forms.NumberInput(attrs={"class": "carnew-form-input"}),
            "model_year": forms.NumberInput(attrs={"class": "carnew-form-input"}),
            "km": forms.NumberInput(attrs={"class": "carnew-form-input"}),
            "fuel": forms.Select(attrs={"class": "carnew-form-input"}),
            "exchange": forms.Select(attrs={"class": "carnew-form-input"}),
            "color": forms.TextInput(attrs={"class": "carnew-form-input"}),
            "value": forms.NumberInput(attrs={"class": "carnew-form-input"}),
            "seller": forms.TextInput(attrs={"class": "carnew-form-input"}),
            "email": forms.EmailInput(attrs={"class": "carnew-form-input"}),
            "contact": forms.TextInput(attrs={"class": "carnew-form-input"}),
            "photo1": forms.ClearableFileInput(attrs={"class": "carnew-file-input"}),
            "photo2": forms.ClearableFileInput(attrs={"class": "carnew-file-input"}),
            "photo3": forms.ClearableFileInput(attrs={"class": "carnew-file-input"}),
            "photo4": forms.ClearableFileInput(attrs={"class": "carnew-file-input"}),
            "photo5": forms.ClearableFileInput(attrs={"class": "carnew-file-input"}),
            "photo6": forms.ClearableFileInput(attrs={"class": "carnew-file-input"}),
        }


# Criação do formulário de interesse
class InterestForm(forms.ModelForm):
    class Meta:
        model = CarInterest
        fields = ['nome', 'email', 'telefone']

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'contato', 'mensagem']


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

