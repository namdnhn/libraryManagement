# Generated by Django 4.2 on 2023-04-22 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0003_alter_staff_account"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False
            ),
        ),
    ]