# Generated by Django 5.0.7 on 2024-07-23 12:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Housekeeper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Age', models.IntegerField()),
                ('nationality', models.CharField(max_length=50)),
                ('pricePerMonth', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='HireRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester_contact', models.CharField(max_length=100)),
                ('request_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.customuser')),
                ('housekeeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hire_requests', to='housekeeper.housekeeper')),
            ],
        ),
        migrations.CreateModel(
            name='RecruitmentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_contact', models.CharField(max_length=100)),
                ('requested_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('housekeeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruitment_requests', to='housekeeper.housekeeper')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_date', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('housekeeper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_requests', to='housekeeper.housekeeper')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.customuser')),
            ],
        ),
    ]
