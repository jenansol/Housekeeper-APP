# Generated by Django 5.0.7 on 2024-08-20 05:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0049_alter_recruitmentrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentrequest',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.status'),
        ),
    ]
