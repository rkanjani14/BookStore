# Generated by Django 4.1.7 on 2023-02-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookservices', '0002_rename_transanction_id_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(upload_to='book/'),
        ),
    ]