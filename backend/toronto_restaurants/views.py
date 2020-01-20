from django.shortcuts import render
from rest_framework import viewsets
from .serializers import RestaurantSerializer
from .models import Restaurant

class RestaurantView(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        queryset = Restaurant.objects.all()

        mainCategory = self.request.query_params.get('mainCategory', None)
        
        if mainCategory is not None:
            queryset = queryset.filter(mainCategory=mainCategory)

        return queryset
