# Generated by Django 2.1 on 2020-03-30 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_auto_20200328_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversations',
            old_name='tripId',
            new_name='trip',
        ),
        migrations.RenameField(
            model_name='guide',
            old_name='userid',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='reviews',
            old_name='tripId',
            new_name='trip',
        ),
    ]
