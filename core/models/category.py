from django.db import models 
from django.utils.text import slugify 
from utils.models import TimeInfo 
from core.models.user import User 


class Category(TimeInfo):
    CATEGORY_STATUS = (
        (0, 'Draft'),
        (1, 'Publish'),
        (2, 'Deleted')
    )
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=25, unique=True, null=True, blank=True)
    status = models.SmallIntegerField(default=0, choices=CATEGORY_STATUS)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Category'


    def __str__(self):
        return self.name 
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Tag(TimeInfo):
    name = models.CharField(max_length=25, unique=True)
    hash_name = models.CharField(max_length=31, unique=True, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Tags:
        db_table = 'tags'
        verbose_name_plural = 'Tag'

    
    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        self.hash_name = "#" + slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
