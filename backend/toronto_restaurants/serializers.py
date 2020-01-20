from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "business_id", "name", "address","latitude",
                  "longitude", "stars", "mainCategory", "generalCategory")
