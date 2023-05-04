# Generated by Django 4.2 on 2023-05-03 08:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0006_alter_bookinfo_book_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="book_id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="bookinfo",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
