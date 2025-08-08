from django.db import models 
from django.utils.text import slugify 
from utils.models import TimeInfo, SEOBasicAbstract
from utils.utils import gen_hex
from tinymce.models import HTMLField
from .category import Category
from .user import User 


PUBLISH_STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Deleted')
)


class Blog(TimeInfo, SEOBasicAbstract):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = HTMLField()
    total_comment = models.IntegerField(default=0)
    pid = models.CharField(max_length=32, unique=True, default=gen_hex)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    thumb = models.ImageField(upload_to='blog/', null=True, blank=True)
    status = models.SmallIntegerField(default=0, choices=PUBLISH_STATUS)

    class Meta:
        verbose_name_plural = 'Blog'
        db_table = 'blogs'


    def __str__(self):
        return self.pid 
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)


class BlogComment(TimeInfo):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    blog = models.ForeignKey(Blog, null=True, on_delete=models.SET_NULL)
    content = HTMLField()
    

    class Meta:
        verbose_name_plural = 'Blog Comment'
        db_table = 'blog_comment'


    def __str__(self):
        return f"{self.id}" 
