# Generated by Django 5.0.7 on 2024-08-14 08:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
