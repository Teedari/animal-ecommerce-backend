# Generated by Django 4.1 on 2022-08-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_payment_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9999),
        ),
    ]
