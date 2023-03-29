from django.db import models
import time
import datetime
from dateutil.parser import parse


class Resource(models.Model):
    RESOURCE_NAME = models.CharField(max_length=255, unique=True)
    RESOURCE_URL = models.CharField(max_length=255, unique=True)
    top_tag = models.JSONField()
    bottom_tag = models.JSONField()
    title_cut = models.JSONField()
    date_cut = models.JSONField()

class Items(models.Model):
    res_id = models.ForeignKey(to=Resource, related_name='items', on_delete=models.CASCADE)
    link = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    content = models.TextField()
    news_unix_date = models.BigIntegerField()
    added_unix_date = models.DateTimeField(auto_now_add=True)
    news_date = models.DateField()
