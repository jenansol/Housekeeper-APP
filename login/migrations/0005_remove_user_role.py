# Generated by Django 5.0.7 on 2024-07-24 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
    ]
