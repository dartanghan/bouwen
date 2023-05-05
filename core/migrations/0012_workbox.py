# Generated by Django 4.2.1 on 2023-05-05 21:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_remove_credito_usado_empresa_debitada"),
    ]

    operations = [
        migrations.CreateModel(
            name="workbox",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("w_inicio", models.DateTimeField(default=datetime.datetime.now)),
                ("w_fim", models.DateTimeField(default=datetime.datetime.now)),
                ("w_titulo", models.CharField(max_length=200)),
                ("w_descricao", models.TextField()),
                ("w_creditos", models.IntegerField(default=1)),
                (
                    "w_empresa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.empresa"
                    ),
                ),
                (
                    "w_usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.usuario"
                    ),
                ),
            ],
            options={
                "ordering": ["w_inicio"],
            },
        ),
    ]
