# Generated by Django 4.1.7 on 2023-04-19 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('book', '0001_initial'),
        ('user', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('rental_date', models.DateField()),
                ('return_date', models.DateField()),
                ('status', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(upload_to='')),
                ('mail', models.CharField(blank=True, max_length=50, null=True)),
                ('create_date', models.DateField()),
                ('position', models.IntegerField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.account')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='store.store')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionItem',
            fields=[
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='staff.transaction')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='book.book')),
            ],
        ),
    ]
