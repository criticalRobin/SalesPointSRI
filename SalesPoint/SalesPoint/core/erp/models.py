from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator

# Create your models here.

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True, verbose_name='Cédula')
    birth = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='Dirección')
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True, verbose_name='Número de teléfono')
    mail = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Correo electrónico')
    GENDER_CHOICES = [
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male', verbose_name='Sexo')
    
    def __str__(self):
        return str(self.names)
    
    class Meta: 
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id'] 
        

class Category(models.Model):
    
    name = models.CharField(max_length=50, verbose_name='Categoria', unique=True)
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']
        

class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    def __str__(self):
        return str(self.name)
    
    class Meta: 
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']    
    

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_sale = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    def __str__(self):
        return str(self.client.dni)
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']
        

class SaleDetails(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    amount = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    def __str__(self):
        return str(self.product.name)
    
    class Meta:
        verbose_name = 'Detalles Venta'
        verbose_name_plural = 'Detalles Ventas'
        ordering = ['id']
