# Generated by Django 5.0.7 on 2024-07-30 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nationality', '0001_initial'),
        ('service_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PericePerNationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0.0)),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nationality.nationallity')),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_type.servicetype')),
            ],
        ),
    ]
