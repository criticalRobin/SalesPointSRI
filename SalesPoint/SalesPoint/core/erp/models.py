from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator
from django.forms import model_to_dict

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
        return f"{self.names} {self.surnames}"
    
    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['birth'] = self.birth.strftime('%Y-%m-%d')
        return item
    
    class Meta: 
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id'] 
        

class Category(models.Model):
    
    name = models.CharField(max_length=50, verbose_name='Categoria', unique=True)
    
    def __str__(self):
        return str(self.name)
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item
    
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
    
    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['image'] = self.image.url if self.image else ''
        item['pvp'] = format(self.pvp, '.2f')
        return item
    
    class Meta: 
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']    
    

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_sale = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    IVA_CHOICES = [
        (0.00, '0.00'),
        (12.00, '12.00'),
    ]
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, choices=IVA_CHOICES)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    def __str__(self):
        return str(self.client.dni)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['client'] = self.client.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_sale'] = self.date_sale.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.saledetails_set.all()]
        return item
    
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
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item
    
    class Meta:
        verbose_name = 'Detalles Venta'
        verbose_name_plural = 'Detalles Ventas'
        ordering = ['id']
