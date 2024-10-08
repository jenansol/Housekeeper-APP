# Generated by Django 5.0.7 on 2024-08-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_alter_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='action',
            field=models.CharField(choices=[('SALE', 'Sale'), ('3DS', '3D Secure'), ('REDIRECT', 'Redirect'), ('REFUND', 'Refund'), ('RECURRING', 'Recurring'), ('sale', 'Sale'), ('refund', 'Refund'), ('GET_TRANS_DETAILS', 'GET_TRANS_DETAILS')], max_length=50),
        ),
    ]
