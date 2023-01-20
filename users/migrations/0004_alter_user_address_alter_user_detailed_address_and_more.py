# Generated by Django 4.1.4 on 2023-01-20 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_detailed_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, default="", max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="detailed_address",
            field=models.CharField(blank=True, default="", max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_nb",
            field=models.CharField(blank=True, default="", max_length=13, null=True),
        ),
    ]
