# Generated by Django 5.0.7 on 2024-08-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, choices=[('3DS', '3D Secure'), ('REDIRECT', 'Redirect'), ('SETTLED', 'Settled'), ('REFUND', 'Refund'), ('DECLINED', 'Declined'), ('PREPARE', 'Prepare'), ('PENDING', 'Pending')], max_length=50, null=True),
        ),
    ]
