# Generated by Django 4.1 on 2022-08-29 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0021_alter_animal_image_slug_1_alter_animal_image_slug_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='phone_number',
            field=models.CharField(default=' ', max_length=10),
            preserve_default=False,
        ),
    ]