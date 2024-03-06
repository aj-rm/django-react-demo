from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission


admin.site.register(Task)
admin.site.register(Permission)