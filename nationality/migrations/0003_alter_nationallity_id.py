# Generated by Django 5.0.7 on 2024-08-10 07:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nationality', '0002_rename_nationallity_nationallity_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationallity',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
