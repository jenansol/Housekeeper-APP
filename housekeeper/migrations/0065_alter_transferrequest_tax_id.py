# Generated by Django 5.0.7 on 2024-08-26 08:47

import django.db.models.deletion
import housekeeper.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0064_alter_recruitmentrequest_tax_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferrequest',
            name='tax_id',
            field=models.ForeignKey(blank=True, default=housekeeper.models.TransferRequest.get_default_taxes, null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.taxes'),
        ),
    ]
