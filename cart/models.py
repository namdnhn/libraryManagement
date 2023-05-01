from django.db import models
from home.models import Account
from book.models import Book
# Create your models here.

class Cart(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.book.info.title + ' ' + self.book.book_id