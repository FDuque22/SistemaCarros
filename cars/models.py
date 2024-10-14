from django.db import models

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):  # Retorna o nome da marca
        return self.name


class Car(models.Model):
    id = models.AutoField(primary_key=True)  # ID automático
    model = models.CharField(max_length=200)  # Modelo do carro
    marca = models.CharField(max_length=200, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='cars', blank=True, null=True)
    seller = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True)
    factory_year = models.IntegerField(blank=True, null=True)  # Ano de fabricação
    model_year = models.IntegerField(blank=True, null=True)  # Ano do modelo
    plate = models.CharField(max_length=20, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)  # Valor do carro
    fuel = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)  # Usar EmailField para emails
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

    def __str__(self):  # Retorna o modelo do carro
        return self.model


class CarInventory(models.Model):
    cars_count = models.IntegerField()
    cars_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação

    class Meta:
        ordering = ['-created_at']  # Ordena por data de criação

    def __str__(self):
        return f'{self.cars_count} - {self.cars_value}'


class CarInterest(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='interests')
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Interesse por {self.car.model} - {self.nome}'
