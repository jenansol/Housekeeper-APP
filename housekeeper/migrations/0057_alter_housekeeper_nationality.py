# Generated by Django 5.0.7 on 2024-08-25 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0056_alter_housekeeper_experience_years_and_more'),
        ('nationality', '0007_alter_nationallity_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekeeper',
            name='nationality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nationality.nationallity'),
        ),
    ]
