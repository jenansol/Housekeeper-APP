# Generated by Django 5.0.7 on 2024-08-20 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0047_recruitmentrequest_requester_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentrequest',
            name='requester_city',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recruitmentrequest',
            name='requester_firstName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recruitmentrequest',
            name='requester_lastName',
            field=models.CharField(max_length=100),
        ),
    ]
