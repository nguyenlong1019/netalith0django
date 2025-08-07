from django.db import models 
from django.utils.text import slugify 
from utils.models import TimeInfo 


class Category(TimeInfo):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=300, null=True, blank=True)


    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Category'


    def __str__(self):
        return self.name 
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
