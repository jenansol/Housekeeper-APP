# Generated by Django 5.0.7 on 2024-08-12 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0021_remove_hirerequest_is_discount_and_more'),
        ('service_type', '0003_servicetype_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='hirerequest',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service_type.servicetype'),
        ),
    ]
