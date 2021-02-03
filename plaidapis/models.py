from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

# Create your models here.


class TokenItem(models.Model):
    access_token = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Log(models.Model):
    request = JSONField(null=True, blank=True)
    response = JSONField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

# can design batter mmodel according to data received


class Transaction(models.Model):
    data = JSONField(null=True, blank=True)


class Account(models.Model):
    data = JSONField(null=True, blank=True)


class Item(models.Model):
    data = JSONField(null=True, blank=True)
