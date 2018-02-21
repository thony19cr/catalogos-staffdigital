from __future__ import unicode_literals

from django.db import models
from marcas.models import Brands


class Product(models.Model):
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=2, blank=True, null=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=200)
    is_variation = models.BooleanField(default=False)
    brand = models.ForeignKey(Brands, verbose_name='Marcas')
    code = models.IntegerField()
    family = models.IntegerField(default=1)
    is_complement = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_visibility = models.BooleanField(default=True)
    price = models.IntegerField(blank=True)
    price_offer = models.IntegerField(blank=True, null=True)
    offer_day_form = models.DateTimeField(auto_now=True, null=True)
    offer_day_to = models.DateTimeField(auto_now=True, null=True)
    quantity = models.IntegerField(blank=True)
    sku = models.IntegerField(blank=True)
    product = models.OneToOneField(Product, verbose_name='Productos', related_name='details')

    def __str__(self):
        return 'Detail'
