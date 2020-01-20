from django.contrib import admin
from .models import HeatMap

class HeatMapAdmin(admin.ModelAdmin):
    list_display = ["x", "y", "probability"]

admin.site.register(HeatMap, HeatMapAdmin)
