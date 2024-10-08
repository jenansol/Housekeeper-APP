# Generated by Django 5.0.7 on 2024-08-17 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0004_alter_contract_payment_details'),
        ('payment', '0014_payment_deleted_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='payment_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.payment'),
        ),
    ]
