# Generated by Django 5.0.7 on 2024-08-13 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0027_remove_housekeeper_request_type_and_more'),
        ('service_type', '0003_servicetype_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='HousekeeperRequestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('housekeeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housekeeper.housekeeper')),
                ('request_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_type.servicetype')),
            ],
        ),
    ]
