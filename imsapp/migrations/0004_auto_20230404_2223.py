# Generated by Django 2.2.4 on 2023-04-04 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imsapp', '0003_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.FloatField(default=1),
        ),
    ]