from django.db import models
from store.models import Store
from home.models import Account
from book.models import Book
from user.models import User
from rest_framework.permissions import BasePermission


# Create your models here.
class Staff(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    picture = models.ImageField()
    mail = models.CharField(max_length=50, blank=True, null=True)
    store = models.ForeignKey(Store, models.DO_NOTHING)
    account = models.OneToOneField(Account, related_name="staff", on_delete=models.CASCADE)
    create_date = models.DateField()
    position = models.IntegerField()

    def __str__(self):
        return self.account.username


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
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


class StaffOnlyPermission(BasePermission):
    message = 'Access denied. Only staff members are allowed.'

    def has_permission(self, request, view):
        print(request.user)
        return request.user and request.user.is_staff
