# Generated by Django 5.0.7 on 2024-08-12 06:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temporary_discount', '0003_custompackage'),
    ]

    operations = [
        migrations.AddField(
            model_name='custompackage',
            name='is_discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='custompackage',
            name='temporary_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='temporary_discount.tempoararydiscount'),
        ),
    ]
