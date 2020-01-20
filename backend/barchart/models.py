from django.db import models

class BarChart(models.Model):
    class Meta:
        managed = True
        db_table = 'barchart'

    category=models.CharField(max_length=30)
    probability=models.FloatField(null=False)
