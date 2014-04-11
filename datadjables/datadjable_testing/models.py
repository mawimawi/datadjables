# encoding: utf-8

from django.db import models
from datetime import date


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=128)
    zip = models.PositiveSmallIntegerField()
    birthdate = models.DateField()

    @property
    def age(self):
        """a "good enough" estimation of the persons age in years)"""
        return int((date.today() - self.birthdate).days / 365.25)


class Product(models.Model):
    name = models.CharField(max_length=128)
    standard_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return u"{0}, Version {1}".format(self.name, self.pk)

    @property
    def short_name(self, name_length=15):
        if len(self.name) > 15:
            name = self.name[:14] + u'…'
        else:
            name = self.name
        return u"{0}, Version {1}".format(name, self.pk)


class Purchase(models.Model):
    buyer = models.ForeignKey("Person")
    product = models.ForeignKey("Product")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    purchase_timestamp = models.DateTimeField()
