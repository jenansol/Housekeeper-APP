# Generated by Django 5.0.7 on 2024-08-10 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_otpmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
