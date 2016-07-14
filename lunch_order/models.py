from __future__ import unicode_literals

from django.db import models


class Orders(models.Model):
    dish = models.CharField(max_length=100)
    byr = models.IntegerField(null=True)
    byn = models.FloatField(null=True)
    comment = models.CharField(max_length=300, blank=True, null=True)


class Customers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
