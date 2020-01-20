from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserClickSerializer
from .models import UserClick
from datetime import datetime


class UserClickView(viewsets.ModelViewSet):
    serializer_class = UserClickSerializer

    def get_queryset(self):
        # Retrieve all user clicks
        user_clicks = UserClick.objects.all()
        username = self.request.query_params.get('username', None)

        if username is not None:
            user_clicks = user_clicks.filter(username=username)

        return user_clicks
