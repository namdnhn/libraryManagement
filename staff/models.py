from django.db import models
from store.models import Store
from home.models import Account
from book.models import Book
from user.models import User


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
