"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from map_view import views as map_view_views
from user_input import views as user_input_views
from toronto_restaurants import views as toronto_restaurants_views
from heatmap import views as heatmap_views
from barchart import views as barchart_views
from users import views as users_views



router = routers.DefaultRouter()
router.register(r'crimes', map_view_views.CrimeCaseView, 'map_view')
router.register(r'user_clicks', user_input_views.UserClickView, 'user_input')
router.register(r'restaurants', toronto_restaurants_views.RestaurantView, 'toronto_restaurants')
router.register(r'heatmap', heatmap_views.HeatMapView, 'heatmap')
router.register(r'barchart', barchart_views.BarChartView, 'barchart')
router.register(r'users', users_views.UsersView, 'users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('heatmap.urls')),
    path('api/', include('barchart.urls'))
]
