from django.db import models
from home.models import Account
from book.models import Book, Bookinfo
from datetime import date, timedelta

from store.models import Store


# Create your models here.

class Cart(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    book = models.ForeignKey(Bookinfo, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.book.title + ' ' + str(self.cart.user.username)


class Transaction(models.Model):
    class Status(models.IntegerChoices):
        WAIT = 1, 'Waiting'
        BORROWING = 2, 'Borrowing'
        DONE = 0, 'Done'

    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    regis_date = models.DateField(default=date.today)
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(default=(date.today() + timedelta(days=7)))
    trans_status = models.IntegerField(choices=Status.choices, default=Status.WAIT)

    def __str__(self):
        return str(self.id)


class TransactionItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.transaction.id)
