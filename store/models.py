from django.db import models

# Create your models here.

class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.id