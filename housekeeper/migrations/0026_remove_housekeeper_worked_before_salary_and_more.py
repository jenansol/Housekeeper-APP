# Generated by Django 5.0.7 on 2024-08-12 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0025_alter_recruitmentrequest_service_type_and_more'),
        ('service_type', '0003_servicetype_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housekeeper',
            name='worked_before_salary',
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='request_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service_type.servicetype'),
        ),
    ]
