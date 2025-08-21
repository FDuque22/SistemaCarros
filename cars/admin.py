from django.contrib import admin
from cars.models import Car, Brand, CarInterest, Contato

# Classe de administração para Brand
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Classe de administração para Car
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'factory_year', 'model_year', 'plate', 'value',)
    search_fields = ('model', 'brand__name',)  # Permite buscar carros pelo modelo e pela marca

# Classe de administração para CarInterest
class CarInterestAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'car')
    search_fields = ('nome',)

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'contato', 'mensagem')
    search_fields = ('nome',)

# Registrando os modelos no painel de administração
admin.site.register(Brand, BrandAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarInterest, CarInterestAdmin)
admin.site.register(Contato, ContatoAdmin)