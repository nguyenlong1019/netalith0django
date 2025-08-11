from django.db import models 
from django.core.validators import FileExtensionValidator 
from django.utils.text import slugify 
import os 
from django.dispatch import receiver 
from utils.models import TimeInfo 
from .user import User 


PUBLISH_STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Deleted')
)


class Game(TimeInfo):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, unique=True)
    status = models.SmallIntegerField(default=1, choices=PUBLISH_STATUS)
    slug = models.SlugField(max_length=300, unique=True, null=True, blank=True)
    javascript = models.TextField()
    css = models.TextField()
    html = models.TextField()
    logo = models.FileField(upload_to='game/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])])
    banner = models.FileField(upload_to='game/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])])
    view_count = models.IntegerField(default=0) 
    play_count = models.IntegerField(default=0)


    class Meta:
        db_table = 'game'
        verbose_name_plural = 'Game'


    def __str__(self):
        return self.name 
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)
