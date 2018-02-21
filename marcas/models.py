from __future__ import unicode_literals

from django.db import models


class Brands(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
