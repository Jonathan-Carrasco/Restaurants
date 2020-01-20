from django.contrib import admin
from .models import BarChart

class BarChartAdmin(admin.ModelAdmin):
    list_display = ("category", "probability")

admin.site.register(BarChart, BarChartAdmin)
