from django.db import models

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):  # Retorna o nome da marca
        return self.name
    
FUEL_CHOICES = [
    ('Gasolina', 'Gasolina'),
    ('Alcool', 'Álcool'),
    ('Flex', 'Flex'),
    ('Diesel', 'Diesel'),
    ('Eletrico', 'Elétrico'),
]

EXCHANGE_CHOICES = [
    ('Manual', 'Manual'),
    ('Automatico', 'Automático'),
]

MARCA_CHOICES = [
    ('Chevrolet', 'Chevrolet'),
    ('Fiat', 'Fiat'),
    ('Volkswagen', 'Volkswagen'),
    ('Ford', 'Ford'),
    ('Renault', 'Renault'),
    ('Hyundai', 'Hyundai'),
    ('Toyota', 'Toyota'),
    ('Honda', 'Honda'),
    ('Nissan', 'Nissan'),
    ('Jeep', 'Jeep'),
    ('Mitsubishi', 'Mitsubishi'),
    ('Peugeot', 'Peugeot'),
    ('Citroen', 'Citroën'),
    ('Kia', 'Kia'),
    ('Bmw', 'BMW'),
    ('Mercedes', 'Mercedes-Benz'),
    ('Audi', 'Audi'),
    ('Volvo', 'Volvo'),
    ('Jac', 'JAC'),
    ('Chery', 'Chery'),
]

CAR_TYPE_CHOICES = (
    ('sedan', 'Sedan'),
    ('suv', 'SUV'),
    ('hatch', 'Hatch'),
    ('pickup', 'Pickup'),
    ('coupé', 'Coupé'),
    ('convertible', 'Convertible'),
)


class Car(models.Model):
    id = models.AutoField(primary_key=True)  # ID automático
    model = models.CharField(max_length=200)  # Modelo do carro
    marca = models.CharField(max_length=50, choices=MARCA_CHOICES, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='cars', blank=True, null=True)
    seller = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=200, blank=True, null=True)
    factory_year = models.IntegerField(blank=True, null=True)  # Ano de fabricação
    model_year = models.IntegerField(blank=True, null=True)  # Ano do modelo
    tipo = models.CharField(
        max_length=20,
        choices=CAR_TYPE_CHOICES,
        blank=True, null=True
    )
    plate = models.CharField(max_length=20, blank=True, null=True)
    value = models.DecimalField(
        max_digits=10,  # total de dígitos
        decimal_places=2,  # casas decimais
        blank=True,
        null=True
    )
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES, blank=True, null=True)
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

    def formatted_value(self):
        if self.value is not None:
            return f"R$ {self.value:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
        return "R$ 0,00"

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
        return f'Interesse por {self.nome} - {self.car.model}'
    
from django.db import models

class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    contato = models.CharField(max_length=15)  # Para o telefone ou número de contato
    mensagem = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Contato de {self.nome}'