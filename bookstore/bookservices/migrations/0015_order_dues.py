# Generated by Django 4.1.7 on 2023-03-04 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookservices', '0014_alter_order_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='dues',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
