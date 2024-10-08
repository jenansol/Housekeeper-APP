# Generated by Django 5.0.7 on 2024-08-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0017_alter_actionlog_id_alter_employmenttype_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmenttype',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='hirerequest',
            name='requester_city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='hirerequest',
            name='requester_firstName',
            field=models.CharField(default='DefaultFirstName', max_length=100),
        ),
        migrations.AddField(
            model_name='hirerequest',
            name='requester_lastName',
            field=models.CharField(default='DefaultLastName', max_length=100),
        ),
        migrations.AddField(
            model_name='religion',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='status',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
