from rest_framework import serializers
from .models import CrimeCase
import json


class CrimeCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeCase
        fields = ('complaint', 'latitude', 'longitude', 'date', 'time', 'crime_code', 'description', 'street_address')
