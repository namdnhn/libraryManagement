# Generated by Django 4.2 on 2023-05-02 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0004_alter_staff_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staff",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="mail",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="picture",
        ),
        migrations.AddField(
            model_name="staff",
            name="avatar",
            field=models.ImageField(
                default="static/des/userava.png", upload_to="static/assets/img/team/"
            ),
        ),
        migrations.AddField(
            model_name="staff",
            name="birthday",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="staff",
            name="fname",
            field=models.CharField(default="Unknown", max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="staff",
            name="gender",
            field=models.PositiveSmallIntegerField(
                blank=True, choices=[(1, "Male"), (2, "Female")], null=True
            ),
        ),
        migrations.AddField(
            model_name="staff",
            name="lname",
            field=models.CharField(default=123, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="staff",
            name="phone",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="staff",
            name="address",
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="staff",
            name="create_date",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='TransactionItem',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
