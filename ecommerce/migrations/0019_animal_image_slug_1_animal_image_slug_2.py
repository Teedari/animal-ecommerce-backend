# Generated by Django 4.1 on 2022-08-25 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0018_remove_category_animal_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='image_slug_1',
            field=models.SlugField(max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='animal',
            name='image_slug_2',
            field=models.SlugField(max_length=225, null=True),
        ),
    ]
