from django.urls import path
from . import views

# Whenever the a request to api/barcharts is made, barchart_list will be called
urlpatterns = [
    path('barcharts/', views.barchart_list)
]
