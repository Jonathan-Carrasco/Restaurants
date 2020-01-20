from rest_framework import serializers
from .models import UserClick


class UserClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClick
        fields = ("id", "time_stamp", "name", "username", "generalCategory", "address", "stars")
