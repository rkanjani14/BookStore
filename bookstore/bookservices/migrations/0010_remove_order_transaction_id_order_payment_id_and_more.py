# Generated by Django 4.1.7 on 2023-03-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookservices', '0009_shippingaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(default='', max_length=36),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='signature_id',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='complete',
            field=models.BooleanField(default='Pending'),
        ),
    ]