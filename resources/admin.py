from django.contrib import admin
from . import models

admin.site.register(models.Items)
admin.site.register(models.Resource)