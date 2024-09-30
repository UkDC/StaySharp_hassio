# Generated by Django 4.1 on 2022-08-22 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stay_sharp", "0002_all_knifes_delete_all_knife"),
    ]

    operations = [
        migrations.AlterField(
            model_name="all_knifes",
            name="CrMoV",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(50),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="all_knifes",
            name="angle",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(40),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="all_knifes",
            name="carbon",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(6),
                ]
            ),
        ),
    ]
