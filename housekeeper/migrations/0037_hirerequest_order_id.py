# Generated by Django 5.0.7 on 2024-08-15 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0036_remove_hirerequest_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hirerequest',
            name='order_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
