# Generated by Django 2.1 on 2020-03-28 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_auto_20200227_1749'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guide',
            old_name='laguages',
            new_name='languages',
        ),
    ]
