# Generated by Django 4.1 on 2022-09-04 06:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stay_sharp", "0016_alter_grinding_data_c1_alter_grinding_data_c2"),
    ]

    operations = [
        migrations.CreateModel(
            name="Account_table",
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
                ("date", models.DateField()),
                ("brand", models.CharField(blank=True, max_length=30, null=True)),
                ("series", models.CharField(blank=True, max_length=30, null=True)),
                ("steel", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "carbon",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(6),
                        ],
                    ),
                ),
                (
                    "CrMoV",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(50),
                        ],
                    ),
                ),
                (
                    "length",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(500),
                        ],
                    ),
                ),
                (
                    "width",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(60),
                        ],
                    ),
                ),
                (
                    "grinding_angle",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(40),
                        ],
                    ),
                ),
                ("honing_add", models.FloatField(blank=True, null=True)),
                ("comments", models.CharField(max_length=100)),
            ],
        ),
    ]
