# Generated by Django 5.1 on 2024-10-27 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dogs", "0009_dog_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dog",
            name="user",
        ),
    ]
