# Generated by Django 4.2.1 on 2023-05-10 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_workbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workbox',
            name='w_creditos',
            field=models.FloatField(default=1),
        ),
    ]
