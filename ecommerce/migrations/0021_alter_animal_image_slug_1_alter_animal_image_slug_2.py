# Generated by Django 4.1 on 2022-08-26 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0020_alter_animal_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='image_slug_1',
            field=models.CharField(max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='image_slug_2',
            field=models.CharField(max_length=225, null=True),
        ),
    ]
