from django.db import models
from home.models import Account
from book.models import Book, Bookinfo
from store.models import Store


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
    avatar = models.ImageField(upload_to="static/assets/img/team/", default='static/des/userava.png')
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    account = models.OneToOneField(Account, related_name="user", on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)
    expired_date = models.DateField(null=True, blank=True)
    current_store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.account.username

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(Bookinfo, on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    

class Rate(models.Model):
    book = models.ForeignKey(Bookinfo, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    score = models.IntegerField()