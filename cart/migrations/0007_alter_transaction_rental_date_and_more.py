# Generated by Django 4.2 on 2023-05-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0006_alter_transaction_rental_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="rental_date",
            field=models.DateField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name="transactionitem",
            name="return_date",
            field=models.DateField(blank=True, default=None),
        ),
    ]
