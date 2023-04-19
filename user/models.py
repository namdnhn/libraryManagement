from django.db import models
from home.models import Account
from book.models import Book, Bookinfo

# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    avatar = models.ImageField()
    mail = models.CharField(unique=True, max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    is_active = models.IntegerField()
    create_date = models.DateField()
    expired_date = models.DateField()

    def __str__(self):
        return self.account.username

class CartItem(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING)

    def __str__(self):
        return self.book.book_id
    
class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    info = models.ForeignKey(Bookinfo, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id