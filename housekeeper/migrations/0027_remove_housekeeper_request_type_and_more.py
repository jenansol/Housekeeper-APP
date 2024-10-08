# Generated by Django 5.0.7 on 2024-08-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0026_remove_housekeeper_worked_before_salary_and_more'),
        ('service_type', '0003_servicetype_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housekeeper',
            name='request_type',
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='experience_years',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='languages_spoken',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='rating',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='housekeeper',
            name='request_types',
            field=models.ManyToManyField(to='service_type.servicetype'),
        ),
    ]
