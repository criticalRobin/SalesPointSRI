# Generated by Django 4.2.2 on 2023-06-21 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='iva',
            field=models.DecimalField(choices=[(0.0, '0.00'), (12.0, '12.00')], decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
