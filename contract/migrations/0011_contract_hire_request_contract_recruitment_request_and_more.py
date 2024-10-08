# Generated by Django 5.0.7 on 2024-08-18 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0010_contract_contract_file'),
        ('housekeeper', '0045_actionlog_custom_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='hire_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.hirerequest'),
        ),
        migrations.AddField(
            model_name='contract',
            name='recruitment_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.recruitmentrequest'),
        ),
        migrations.AddField(
            model_name='contract',
            name='transfer_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.transferrequest'),
        ),
    ]
