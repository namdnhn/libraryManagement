# Generated by Django 4.2 on 2023-04-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="email",
            field=models.CharField(default="NULL", max_length=50),
            preserve_default=False,
        ),
    ]