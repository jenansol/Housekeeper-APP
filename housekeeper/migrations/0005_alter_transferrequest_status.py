# Generated by Django 5.0.7 on 2024-07-28 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0004_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferrequest',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housekeeper.status'),
        ),
    ]
