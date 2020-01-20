from django.db import models
import datetime


class Restaurant(models.Model):
    """A table to store restaurant data, in case it is needed outside the JSON.

    Each field of this table, including the id, should match up with existing
    information in the Yelp dataset JSON file."""


    id = models.IntegerField(primary_key=True)
    business_id = models.CharField(max_length=50, null=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=75, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    stars = models.FloatField(null=False)
    mainCategory = models.CharField(max_length=50, null=False)
    generalCategory = models.CharField(max_length=50, null=False)

    class Meta:
        managed = True
        db_table = 'tr_general'
