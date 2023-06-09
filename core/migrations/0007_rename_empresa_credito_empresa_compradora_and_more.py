# Generated by Django 4.2.1 on 2023-05-04 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_credito_credito_dt_uso"),
    ]

    operations = [
        migrations.RenameField(
            model_name="credito",
            old_name="empresa",
            new_name="empresa_compradora",
        ),
        migrations.RemoveField(
            model_name="credito",
            name="credito_adquirido",
        ),
        migrations.RemoveField(
            model_name="credito",
            name="credito_dt_uso",
        ),
        migrations.RemoveField(
            model_name="credito",
            name="credito_usado",
        ),
        migrations.AddField(
            model_name="credito",
            name="credito_finalizado",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="credito_usado",
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
                ("credito_usado_dt", models.DateTimeField(auto_now=True)),
                ("credito_usado_parcial", models.BooleanField(default=False)),
                (
                    "credito",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.credito"
                    ),
                ),
                (
                    "empresa_creditada",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="empresa_creditada",
                        to="core.empresa",
                    ),
                ),
                (
                    "empresa_debitada",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="empresa_debitada",
                        to="core.empresa",
                    ),
                ),
            ],
        ),
    ]
