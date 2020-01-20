from django.db import models

class HeatMap(models.Model):
    class Meta:
        managed = True
        db_table = 'heatmap'

    x=models.FloatField(null=False)
    y=models.FloatField(null=False)
    probability=models.FloatField(null=False)
