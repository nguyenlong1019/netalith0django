from django.db import models 
from utils.models import TimeInfo 


class Game(TimeInfo):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)
    javascript = models.TextField()
    css = models.TextField()
    html = models.TextField()
    logo = None 
    view_count = None 
    play_count = None 
