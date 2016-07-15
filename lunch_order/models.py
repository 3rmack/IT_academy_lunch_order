from __future__ import unicode_literals

from django.db import models


class Orders(models.Model):
    dish = models.CharField(max_length=100)
    byr = models.IntegerField(null=True, blank=True)
    byn = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=300, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
