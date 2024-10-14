from django.contrib import admin
from cars.models import Car, Brand #Importar modolos dos Carros - Car

# Habilitar no painel de Adm a opção de add carros

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'plate', 'value', 'active',)
    search_fields = ('model', 'brand',) #Buscar Carros pelo Modelo

admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin) #Chama Para Habilitar no Painel Adm


