# Generated by Django 4.2.2 on 2023-07-13 23:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_entity_product_iva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='iva',
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Solo se permiten letras')], verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True, validators=[django.core.validators.RegexValidator(code='invalid_address', message='La dirección no debe contener caracteres especiales.', regex='^[A-Za-z0-9\\s]+$')], verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='client',
            name='mail',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, validators=[django.core.validators.EmailValidator(code='invalid_email', message='El correo electrónico no es válido.')], verbose_name='Correo electrónico'),
        ),
        migrations.AlterField(
            model_name='client',
            name='names',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Solo se permiten letras')], verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator(code='invalid_phone', message='El número de teléfono debe contener solo números.', regex='^[0-9]+$')], verbose_name='Número de teléfono'),
        ),
        migrations.AlterField(
            model_name='client',
            name='surnames',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Solo se permiten letras')], verbose_name='Apellidos'),
        ),
    ]