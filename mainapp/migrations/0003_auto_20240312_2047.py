# Generated by Django 3.0.1 on 2024-03-12 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_paymentsactivated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentsactivated',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]
