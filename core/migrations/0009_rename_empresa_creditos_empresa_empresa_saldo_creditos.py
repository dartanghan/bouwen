# Generated by Django 4.2.1 on 2023-05-04 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_empresa_empresa_creditos"),
    ]

    operations = [
        migrations.RenameField(
            model_name="empresa",
            old_name="empresa_creditos",
            new_name="empresa_saldo_creditos",
        ),
    ]