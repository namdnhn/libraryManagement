from django.db import models
from store.models import Store

# Create your models here.

class Bookinfo(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    publisher = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    cover_price = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return self.id

class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_image = models.ImageField()
    info = models.ForeignKey(Bookinfo, models.DO_NOTHING)
    store = models.ForeignKey(Store, models.DO_NOTHING)
    status = models.IntegerField()

    def __str__(self):
        return self.book_id

