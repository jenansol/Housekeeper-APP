# Generated by Django 5.0.7 on 2024-08-31 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0068_hirerequest_contract_file_hirerequest_dateofbirth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekeeper',
            name='Identification_number',
            field=models.CharField(default='000000000000000000000', max_length=150, unique=True),
        ),
    ]
