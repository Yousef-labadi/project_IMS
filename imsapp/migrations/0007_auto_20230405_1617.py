# Generated by Django 2.2.4 on 2023-04-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imsapp', '0006_order_quantity_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.FloatField(),
        ),
    ]