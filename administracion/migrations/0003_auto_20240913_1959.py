# Generated by Django 2.1.15 on 2024-09-13 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_auto_20240913_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartamenu',
            name='id_plato',
            field=models.IntegerField(),
        ),
    ]
