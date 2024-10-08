# Generated by Django 5.0.7 on 2024-08-06 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, unique=True),
        ),
    ]
