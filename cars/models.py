from django.db import models


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):  #Vai retornar com a marca do carro
        return self.name
    
class Car(models.Model):
    id = models.AutoField(primary_key=True) #Primeiro Campo, ID Automoático
    model = models.CharField(max_length=200)  #Modelo Do Carro, Campo de Texto, (200 Caracteres)
    marca = models.CharField(max_length=200, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='Car_Brand', blank=True, null=True)
    seller = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True) 
    #Marca do Carro - Chave Estrangeira(On - Não Deleta se tiver carro cadastrado - Nome da Relação)
    factory_year = models.IntegerField(blank=True, null=True) #Ano de Fabricação do Carro (Campo Não Obrigatório)
    model_year = models.IntegerField(blank=True, null=True) #Ano de Modelo do Carro (Campo Não Obrigatório)
    plate = models.CharField(max_length=20, blank=True, null=True)
    value = models.FloatField(blank=True, null=True) #Valor do Carro, Ponto Flutuante (Campo Não Obrigatório)
    fuel = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    km = models.CharField(max_length=20, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    photo1 = models.ImageField(upload_to='cars/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='cars/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='cars/', blank=True, null=True)
    photo4 = models.ImageField(upload_to='cars/', blank=True, null=True)
    photo5 = models.ImageField(upload_to='cars/', blank=True, null=True)
    photo6 = models.ImageField(upload_to='cars/', blank=True, null=True)
    active = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):  #Vai retornar com o Modelo do Carro
        return self.model
    

class CarInventory(models.Model):
    cars_count = models.IntegerField()
    cars_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True) #Qualquer registro que entrar, ele ja colocar a data.

    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'