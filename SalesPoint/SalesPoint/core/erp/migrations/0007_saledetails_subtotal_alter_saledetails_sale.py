# Generated by Django 4.2.2 on 2023-07-14 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_remove_saledetails_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='saledetails',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='saledetails',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='erp.sale'),
        ),
    ]