# Generated by Django 5.0.7 on 2024-08-12 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0022_hirerequest_service_type'),
        ('service_type', '0003_servicetype_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruitmentrequest',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service_type.servicetype'),
        ),
        migrations.AddField(
            model_name='recruitmentrequest',
            name='total_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='transferrequest',
            name='service_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='service_type.servicetype'),
        ),
        migrations.AddField(
            model_name='transferrequest',
            name='total_price',
            field=models.FloatField(default=0.0),
        ),
    ]
