from django.shortcuts import render
from decimal import Decimal
from django.db import models
from datetime import datetime
from django.core.validators import MinLengthValidator
from django.forms import model_to_dict
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from configs.settings import STATIC_URL
from configs.settings import MEDIA_URL

# Create your models here.


class Entity(models.Model):
    ruc = models.CharField(max_length=13, verbose_name="RUC", unique=True)
    social_reason = models.CharField(max_length=50, verbose_name="Razón Social")
    commercial_name = models.CharField(max_length=50, verbose_name="Nombre Comercial")
    main_address = models.CharField(max_length=50, verbose_name="Dirección Matriz")
    stablishement_address = models.CharField(
        max_length=50, verbose_name="Dirección Establecimiento"
    )
    stablishement_code = models.CharField(
        max_length=3, verbose_name="Código Establecimiento"
    )
    emition_point_code = models.CharField(
        max_length=3, verbose_name="Código Punto de Emisión"
    )
    CONTABILITY_CHOICES = [
        ("SI", "SI"),
        ("NO", "NO"),
    ]
    contability_obligation = models.CharField(
        max_length=2,
        choices=CONTABILITY_CHOICES,
        verbose_name="Obligado a llevar contabilidad",
    )
    logo = models.ImageField(upload_to="product/%Y/%m/%d", null=True, blank=True)
    ENVIROMENT_CHOICES = [
        ("PRODUCCION", "PRODUCCION"),
        ("PRUEBAS", "PRUEBAS"),
    ]
    enviroment = models.CharField(
        max_length=10, choices=ENVIROMENT_CHOICES, verbose_name="Entorno"
    )
    
    def get_logo(self):
        if self.logo:
            return '{}{}'.format(MEDIA_URL, self.logo)
        return '{}{}'.format(STATIC_URL, 'img/noviaaaa.jpg')
    
    def get_commercial_name(self):
        return self.commercial_name if self.commercial_name else ""

    def my_view(request):
        my_entity = Entity.objects.get(pk=1)

        context = {
            'request': request,
            'logo_url': my_entity.get_logo(),  # Agregamos el logo como 'logo_url'
            'commercial_name': my_entity.get_commercial_name(),  # Agregamos el nombre comercial
        }

        return render(request, 'sidebar.html', context)
    
    def __str__(self):
        return f"{self.social_reason}"

    class Meta:
        verbose_name = "Entidad"
        verbose_name_plural = "Entidades"
        ordering = ["id"]


dni_regex = r"^\d{10}$"


def ecuadorian_dni_validator(dni):
    if re.match(dni_regex, dni):
        province = int(dni[0:2])
        if province >= 1 and province <= 24:
            return True
    return False

def passport_validator(passport_number):
    passport_pattern = r"^[a-zA-Z0-9]{6,}$"
    return bool(re.match(passport_pattern, passport_number))


class Client(models.Model):
    names = models.CharField(
        max_length=150,
        verbose_name="Nombres",
        validators=[RegexValidator(r"^[a-zA-Z]*$", "Solo se permiten letras")],
    )
    surnames = models.CharField(
        max_length=150,
        verbose_name="Apellidos",
        validators=[RegexValidator(r"^[a-zA-Z]*$", "Solo se permiten letras")],
    )
    ID_TYPE_CHOICES = [
        ("Cedula", "Cédula"),
        ("RUC", "RUC"),
        ("Pasaporte", "Pasaporte"),
    ]
    id_type = models.CharField(
        max_length=10, choices=ID_TYPE_CHOICES, default="Cedula", verbose_name="Tipo de Identificación"
    )
    dni = models.CharField(
        max_length=13,  # Aumenta la capacidad del campo para permitir más caracteres
        validators=[
            MinLengthValidator(6),  # Ajusta el valor según el requisito mínimo para identificaciones, como el pasaporte
        ],
        unique=True,
        verbose_name="Cédula, RUC o Pasaporte",
    )
    birth = models.DateField(default=datetime.now, verbose_name="Fecha de nacimiento")

    address_regex = r"^[A-Za-z0-9\s]+$"
    address_validator = RegexValidator(
        regex=address_regex,
        message="La dirección no debe contener caracteres especiales.",
        code="invalid_address",
    )
    address = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Dirección",
        validators=[address_validator],
    )

    phone_regex = r"^[0-9]+$"
    phone_validator = RegexValidator(
        regex=phone_regex,
        message="El número de teléfono debe contener solo números.",
        code="invalid_phone",
    )
    
    phone = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), phone_validator],
        unique=True,
        verbose_name="Número de teléfono",
    )
    
    email_validator = EmailValidator(
        message='El correo electrónico no es válido.',
        code='invalid_email',
    )
    
    mail = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Correo electrónico",
        validators=[email_validator],
    )
    GENDER_CHOICES = [
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Otro", "Otro"),
    ]
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default="Masculino", verbose_name="Sexo"
    )

    def clean(self):
        super().clean()

        if self.id_type == "Cedula":
            if not ecuadorian_dni_validator(self.dni):
                raise ValidationError("La cédula no es válida para Ecuador.")

        elif self.id_type == "RUC":
            if not self.dni.isdigit() or len(self.dni) != 13:
                raise ValidationError("El RUC debe contener 13 dígitos numéricos válidos.")

        elif self.id_type == "Pasaporte":
            if not passport_validator(self.dni):
                raise ValidationError("El número de pasaporte no es válido.")           

        else:
            raise ValidationError("Tipo de identificación no válido.")

    def __str__(self):
        return f"{self.names} {self.surnames}"

    def toJSON(self):
        item = model_to_dict(self)
        item["gender"] = {"id": self.gender, "name": self.get_gender_display()}
        item["birth"] = self.birth.strftime("%Y-%m-%d")
        return item

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["id"]


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Categoria",
        unique=True,
        validators=[RegexValidator(r"^[a-zA-Z]*$", "Solo se permiten letras")],
    )

    def __str__(self):
        return str(self.name)

    def toJSON(self):
        item = model_to_dict(self, exclude=["user_creation", "user_updated"])
        return item

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["id"]


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre", unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/%Y/%m/%d", null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    IVA_CHOICES = [
        ("0.00", "0.00"),
        ("12.00", "12.00"),
    ]
    iva = models.CharField(max_length=5, choices=IVA_CHOICES, default="0.00")
    sale_price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.name)
    
    def calculate_sale_price(self):
        pvp = self.pvp
        decimal_iva = Decimal(self.iva) / 100
        price_iva = pvp * (1 + decimal_iva)
        return price_iva
    
    def save(self, *args, **kwargs):
        self.sale_price = self.calculate_sale_price()
        super().save(*args, **kwargs)

    def toJSON(self):
        item = model_to_dict(self, exclude="image")
        item["category"] = self.category.toJSON()
        item["image"] = self.image.url if self.image else ""
        item["pvp"] = format(self.pvp, ".2f")
        item["sale_price"] = format(self.calculate_sale_price(), ".2f")
        return item

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["id"]


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_sale = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.client.dni)

    def calculate_total(self):
        self.subtotal = sum([Decimal(detail.subtotal) for detail in self.details.all()])
        self.total = self.subtotal

        for detail in self.details.all():
            product = detail.product
            iva = Decimal(product.iva)
            self.total += detail.subtotal * (iva / 100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guardar la instancia antes de acceder a los detalles
        self.calculate_total()
        super().save(*args, **kwargs)  # Guardar nuevamente para actualizar los campos calculados

    def toJSON(self):
        item = model_to_dict(self)
        item["client"] = self.client.toJSON()
        item["subtotal"] = format(self.subtotal, ".2f")
        item["total"] = format(self.total, ".2f")
        item["date_sale"] = self.date_sale.strftime("%Y-%m-%d")
        item["det"] = [i.toJSON() for i in self.details.all()]
        return item

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["id"]


class SaleDetails(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    amount = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.product.name)

    def calculate_subtotal(self):
        self.subtotal = self.price * self.amount
        iva = Decimal(self.product.iva)
        self.total = Decimal(self.subtotal) * Decimal(1 + (iva / 100))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guardar la instancia antes de calcular el subtotal
        self.calculate_subtotal()
        super().save(*args, **kwargs)  # Guardar nuevamente para actualizar el subtotal

    def toJSON(self):
        item = model_to_dict(self, exclude=["sale"])
        item['product'] = self.product.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = "Detalles Venta"
        verbose_name_plural = "Detalles Ventas"
        ordering = ["id"]
