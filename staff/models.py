from django.db import models
from store.models import Store
from home.models import Account
from book.models import Book
from user.models import User


# Create your models here.
class Staff(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]

    id = models.AutoField(primary_key=True, auto_created=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to="static/assets/img/team/", default='static/des/userava.png')
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.TextField(max_length=255, blank=True, null=True)
    account = models.OneToOneField(Account, related_name="staff", on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    store = models.ForeignKey(Store, models.DO_NOTHING)
    position = models.IntegerField()

    def __str__(self):
        return self.account.username


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    rental_date = models.DateField()
    return_date = models.DateField()
    status = models.IntegerField()

    def __str__(self):
        return self.id


class TransactionItem(models.Model):
    transaction = models.OneToOneField(Transaction, models.DO_NOTHING, primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING)

    def __str__(self):
        return self.book.book_id
