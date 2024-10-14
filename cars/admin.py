from django.contrib import admin
from cars.models import Car, Brand, CarInterest

# Classe de administração para Brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Classe de administração para Car
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'plate', 'value', 'active',)
    search_fields = ('model', 'brand__name',)  # Permite buscar carros pelo modelo e pela marca

# Classe de administração para CarInterest
class CarInterestAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'car')  # Campos a serem exibidos na lista
    search_fields = ('nome', 'email', 'brand__name')  # Permite buscar interesses pelo nome, email e modelo do carro

# Registrando os modelos no painel de administração
admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarInterest, CarInterestAdmin)  # Registrando o modelo CarInterest
