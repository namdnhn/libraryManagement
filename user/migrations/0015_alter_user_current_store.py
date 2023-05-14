# Generated by Django 4.1.7 on 2023-05-14 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_store_id'),
        ('user', '0014_alter_comment_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='current_store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
    ]
