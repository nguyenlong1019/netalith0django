from django.db import models 
from utils.models import TimeInfo, SEOBasicAbstract
from utils.utils import gen_hex
from tinymce.models import HTMLField
from .category import Category
from .user import User 


class Post(TimeInfo):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    feed = HTMLField()
    total_react = models.IntegerField(default=0)
    total_comment = models.IntegerField(default=0)
    pid = models.CharField(max_length=32, unique=True, default=gen_hex)

    class Meta:
        verbose_name_plural = 'Post'
        db_table = 'posts'


    def __str__(self):
        return self.pid 


class PostComment(TimeInfo):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    content = HTMLField()
    

    class Meta:
        verbose_name_plural = 'Post Comment'
        db_table = 'post_comment'


    def __str__(self):
        return f"{self.id}" 
    

class PostReact(TimeInfo):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


    class Meta:
        verbose_name_plural = 'Post React'
        db_table = 'post_react'


    def __str__(self):
        return f"{self.id}" 
