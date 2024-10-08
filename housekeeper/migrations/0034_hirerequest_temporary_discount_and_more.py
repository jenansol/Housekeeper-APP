# Generated by Django 5.0.7 on 2024-08-15 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0033_rename_service_type_hirerequest_request_type_and_more'),
        ('temporary_discount', '0011_remove_custompackage_worked_before_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hirerequest',
            name='temporary_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='temporary_discount.tempoararydiscount'),
        ),
        migrations.AddField(
            model_name='recruitmentrequest',
            name='temporary_discount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='temporary_discount.tempoararydiscount'),
        ),
    ]
