from django.contrib import admin

from .models import Person, Office, Area, Request

# Register your models here.

admin.site.register(Person)
admin.site.register(Office)
admin.site.register(Area)
admin.site.register(Request)
