# Generated by Django 5.0.7 on 2024-08-25 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nationality', '0006_nationallity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationallity',
            name='Nationality',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
