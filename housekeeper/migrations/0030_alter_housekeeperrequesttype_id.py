# Generated by Django 5.0.7 on 2024-08-13 07:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0029_remove_housekeeper_request_types_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekeeperrequesttype',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
