# Generated by Django 4.2 on 2023-11-26 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_orderdetail_amount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderDetail',
        ),
    ]
