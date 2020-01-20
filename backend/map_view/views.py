from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CrimeCaseSerializer
from .models import CrimeCase
from datetime import datetime


class CrimeCaseView(viewsets.ModelViewSet):
    serializer_class = CrimeCaseSerializer

    def get_queryset(self):
        queryset = CrimeCase.objects.all()
        crime_code = self.request.query_params.get('crime_code', None)

        sdate = self.request.query_params.get('sdate', None)
        edate = self.request.query_params.get('edate', None)

        if sdate is not None and edate is not None:
            start_date = datetime.strptime(sdate, '%Y-%m-%d').date()
            end_date = datetime.strptime(edate, '%Y-%m-%d').date()
            queryset = queryset.filter(date__range=(start_date, end_date))

        return queryset
