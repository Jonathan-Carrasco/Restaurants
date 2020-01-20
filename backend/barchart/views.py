from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BarChartSerializer
from .models import BarChart
from django.http import JsonResponse

from sklearn.externals import joblib
from rest_framework.decorators import api_view

class BarChartView(viewsets.ModelViewSet):
    serializer_class = BarChartSerializer

    def get_queryset(self):
        queryset = Barchart.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        return queryset

'''
Loads model for 'username' and retrieves the domains and mu whenever
a get request is made. This information is then serialized and
displayed in json format.
'''

@api_view(['GET'])
def barchart_list(request):
    username = request.GET['username']

    # Dirchilet model for 'username' is retrieved from models folder
    dm = joblib.load(username+"_dm")

    # Array of Barchart models, describing probabilities of each respective category
    barchart = [BarChart(category=category,probability=probability) for category, probability in zip(dm.domains.tolist(), dm.mu.tolist())]

    # Serialize all fields in Barchart model
    serializer = BarChartSerializer(barchart, many=True)

    # Return the serialized information in json format
    return JsonResponse(serializer.data, safe=False)
