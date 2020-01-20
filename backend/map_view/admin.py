from django.contrib import admin
from .models import  CrimeCase

# Register your models here.


class CrimeCaseAdmin(admin.ModelAdmin):
    list_display = ("complaint", "latitude", "longitude", "date", "time", "crime_code", "description")


admin.site.register(CrimeCase, CrimeCaseAdmin)
