# Generated by Django 4.1.4 on 2023-01-30 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dms", "0003_remove_chattingroom_receiver_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chattingroom",
            old_name="user",
            new_name="users",
        ),
    ]