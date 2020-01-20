from django.urls import path
from . import views

# Whenever the a request to api/heatmaps is made, heatmap_list will be called
urlpatterns = [
    path('heatmaps/', views.heatmap_list)
]
