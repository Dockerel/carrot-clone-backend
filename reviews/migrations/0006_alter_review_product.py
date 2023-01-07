# Generated by Django 4.1.4 on 2023-01-07 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_alter_product_buyer"),
        ("reviews", "0005_alter_review_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="product",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="products.product",
            ),
        ),
    ]
