# Generated by Django 5.0.7 on 2024-08-15 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0041_alter_hirerequest_request_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recruitmentrequest',
            old_name='requested_date',
            new_name='request_date',
        ),
        migrations.RenameField(
            model_name='transferrequest',
            old_name='requested_date',
            new_name='request_date',
        ),
    ]
