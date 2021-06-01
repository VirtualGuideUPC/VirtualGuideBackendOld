from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)


class Account(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)  
    email = models.CharField(max_length=70, unique=True, default="")
    password = models.CharField(max_length=255)
    token_notification = models.CharField(max_length=70, default="")
    country = models.ForeignKey(Country, null=False, blank=False, default="1", on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    birthday = models.DateField(default="2021-08-17")
    is_foreign = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    