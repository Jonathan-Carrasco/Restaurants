from django.db import models

class CrimeCase(models.Model):
    complaint = models.IntegerField(primary_key=True)
    district = models.IntegerField(null=False)
    crime_code = models.CharField(max_length=20, null=False)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    street_address = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    class Meta:
        managed = True
        db_table = 'crime_case'

    def serialize(self):
        return {
            'Complaint': int(self.complaint),
            'district': int(self.district),
            'crimeCode': str(self.crime_code).rjust(6, '0'),
            'streetAddress': None if self.street_address is None else str(self.street_address),
            'description': str(self.description),
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'date': self.date,
            'year': self.date.year,
            'month': self.date.month,
            'day': self.date.day,
            'hour': self.time.hour,
            'minute': self.time.minute
        }
