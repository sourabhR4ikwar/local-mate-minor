# Generated by Django 2.1 on 2020-04-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0010_auto_20200330_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='paymentVerified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trips',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]
