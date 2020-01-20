from django.db import models

class Users(models.Model):
    class Meta:
        managed = True
        db_table = 'users'

    username = models.CharField(max_length=50,primary_key=True)
    timestamp=models.IntegerField()
