from django.contrib import admin
from .models import UserClick


class UserClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_stamp', 'name', 'username', 'generalCategory', 'address', 'stars')

admin.site.register(UserClick, UserClickAdmin)
