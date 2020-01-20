from rest_framework import serializers
from .models import BarChart

class BarChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarChart
        fields = ('category','probability')
