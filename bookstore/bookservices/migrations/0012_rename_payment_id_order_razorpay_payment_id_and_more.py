# Generated by Django 4.1.7 on 2023-03-01 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookservices', '0011_alter_order_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment_id',
            new_name='razorpay_payment_id',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='signature_id',
            new_name='razorpay_signature_id',
        ),
    ]
