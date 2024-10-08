# Generated by Django 5.0.7 on 2024-08-01 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0010_housekeeper_worked_before_alter_hirerequest_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='gender',
            field=models.CharField(choices=[('female', 'Female'), ('male', 'Male')], default='female', max_length=50),
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='montly_salary',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='pricePerMonth',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='worked_before_salary',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='employment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.employmenttype'),
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='religion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='housekeeper.religion'),
        ),
    ]
