# Generated by Django 4.1.7 on 2023-02-28 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookservices', '0007_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
