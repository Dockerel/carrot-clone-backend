# Generated by Django 4.1.4 on 2023-01-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="review_exists",
            field=models.BooleanField(default=False),
        ),
    ]
