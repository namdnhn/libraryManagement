# Generated by Django 4.1.7 on 2023-04-20 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_image',
        ),
        migrations.AddField(
            model_name='bookinfo',
            name='book_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
