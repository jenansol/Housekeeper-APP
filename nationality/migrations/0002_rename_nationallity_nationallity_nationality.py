# Generated by Django 5.0.7 on 2024-07-30 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nationality', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nationallity',
            old_name='Nationallity',
            new_name='Nationality',
        ),
    ]
