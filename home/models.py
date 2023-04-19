from django.db import models

# Create your models here.
class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username