from django.contrib import admin
from .models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "business_id", "name", "address", "latitude",
                    "longitude", "stars", "mainCategory", 'generalCategory')


admin.site.register(Restaurant, RestaurantAdmin)
