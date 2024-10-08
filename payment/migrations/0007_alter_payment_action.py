# Generated by Django 5.0.7 on 2024-08-05 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_alter_payment_trans_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='action',
            field=models.CharField(choices=[('SALE', 'Sale'), ('3DS', '3D Secure'), ('REDIRECT', 'Redirect'), ('REFUND', 'Refund'), ('RECURRING', 'Recurring'), ('sale', 'Sale'), ('refund', 'Refund')], max_length=50),
        ),
    ]
