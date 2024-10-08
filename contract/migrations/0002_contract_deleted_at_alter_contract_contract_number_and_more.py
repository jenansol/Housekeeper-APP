# Generated by Django 5.0.7 on 2024-08-17 07:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
        ('login', '0027_blacklistedtoken_deleted_at_otpmessage_deleted_at'),
        ('payment', '0014_payment_deleted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='contract_number',
            field=models.CharField(blank=True, max_length=5, unique=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.payment', unique=True),
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('interest_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('clicked', 'Clicked'), ('abandoned', 'Abandoned')], max_length=20)),
                ('device_info', models.CharField(blank=True, max_length=255, null=True)),
                ('session_data', models.JSONField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='login.customuser')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
