# Generated by Django 5.0.7 on 2024-08-17 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0043_remove_recruitmentrequest_pericepernationality_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionlog',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employmenttype',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hirerequest',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='housekeeperrequesttype',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='recruitmentrequest',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='religion',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transferrequest',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
