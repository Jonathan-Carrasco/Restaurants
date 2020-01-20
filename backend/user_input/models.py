from django.db import models


class UserClick(models.Model):
    time_stamp = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    name = models.CharField(max_length=50, null=False)
    stars = models.FloatField(null=False)
    username = models.CharField(max_length=50, null=False)
    generalCategory = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=75, null=False)


    class Meta:
        managed = True
        db_table = 'user_input'
