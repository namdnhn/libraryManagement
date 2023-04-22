from django.db import models
from home.models import Account
from book.models import Book, Bookinfo


# Create your models here.
class User(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
    ]

    id = models.AutoField(primary_key=True, auto_created=True)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to="home/img/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    account = models.OneToOneField(Account, related_name="user", on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    expired_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.account.username

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else 'static/des/userava.png'


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
