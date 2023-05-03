from django.db import models
from store.models import Store
import uuid


# Create your models here.
class Bookinfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    book_image = models.ImageField(upload_to='static/assets/img/book', default='static/des/book_cover.png', null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    cover_price = models.IntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def __str__(self):
        return self.title


class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    info = models.ForeignKey(Bookinfo, models.DO_NOTHING)
    store = models.ForeignKey(Store, models.DO_NOTHING)
    status = models.IntegerField()

    def __str__(self):
        return self.info.title + ' ' + str(self.book_id)
