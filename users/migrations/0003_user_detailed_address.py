# Generated by Django 4.1.4 on 2023-01-20 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_avatar_alter_user_phone_nb"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="detailed_address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
