import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    last_login, first_name, last_name = (None,) * 3

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
