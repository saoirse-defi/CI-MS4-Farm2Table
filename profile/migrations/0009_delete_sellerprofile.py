# Generated by Django 3.2.7 on 2021-10-10 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20211009_1059'),
        ('profile', '0008_county'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SellerProfile',
        ),
    ]
