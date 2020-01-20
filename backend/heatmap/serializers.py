from rest_framework import serializers
from .models import HeatMap

class HeatMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatMap
        fields = ('x','y','probability')
