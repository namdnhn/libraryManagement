# Generated by Django 4.1.7 on 2023-04-20 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_book_book_image_bookinfo_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
