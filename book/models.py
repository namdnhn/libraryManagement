from django.db import models
from store.models import Store


# Create your models here.

class Bookinfo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    book_image = models.ImageField(upload_to='static/assets/img/book', default=None, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100)
    pages = models.IntegerField(default=0)
    cover_price = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return self.title


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    info = models.ForeignKey(Bookinfo, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.info.title + ' ' + str(self.book_id)
