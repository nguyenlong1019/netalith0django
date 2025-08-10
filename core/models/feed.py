from django.db import models 
from django.db.models import Q 
from django.utils.text import slugify 
from django.core.exceptions import ValidationError 
from django.core.validators import FileExtensionValidator
from utils.models import TimeInfo, SEOBasicAbstract 
from utils.utils import gen_hex 
from tinymce.models import HTMLField 
from .category import Category, Tag 
from .user import User 
import time 


PUBLISH_STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Deleted')
)


class Feed(TimeInfo, SEOBasicAbstract):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=15, default='feed', choices=(('feed', 'Feed'), ('academic', 'Academic')), db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'status': 1},)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    content = HTMLField(null=True, blank=True)
    status = models.SmallIntegerField(default=0, choices=PUBLISH_STATUS)
    total_comment = models.IntegerField(default=0)
    total_view = models.IntegerField(default=0)
    total_react = models.IntegerField(default=0)
    banner = models.FileField(upload_to='feed/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])])
    pid = models.CharField(max_length=32, unique=True, default=gen_hex)
    has_detail = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Feed'
        db_table = 'feeds'
        indexes = [
            models.Index(fields=['type', 'status', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                name='content_required_for_academic_not_null',
                check=~Q(type='academic') | Q(content__isnull=False),
            ),
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug_when_present',
                condition=Q(slug__isnull=False),
            ),
        ]


    def __str__(self):
        return self.pid 
    

    @property
    def total_rank(self):
        return self.total_comment + self.total_view + self.total_react 
    

    def clean(self):
        if self.category and self.category.status != 1:
            raise ValidationError({'category': 'Category must be Published.'})
        if self.type == 'academic':
            if not self.content or not str(self.content).strip():
                raise ValidationError({'content': 'Content is required with Academic type.'})
        if self.type == 'academic' and (not self.title or not self.title.strip()):
            raise ValidationError({'title': 'Title is required with Academic type.'})


    def save(self, *args, **kwargs):
        self.full_clean()
        
        if not self.slug:
            is_title_exists = Feed.objects.filter(title=self.title).exists()
            if is_title_exists:
                self.slug = slugify(self.title) + "_" + f"{time.time() * 1000}"
            else:
                self.slug = slugify(self.title)
        if self.content:
            self.has_detail = True
        else:
            self.has_detail = False 
        super(Feed, self).save(*args, **kwargs)


class FeedComment(TimeInfo):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    feed = models.ForeignKey(Feed, null=True, on_delete=models.SET_NULL)
    content = HTMLField()


    class Meta:
        verbose_name_plural = 'Feed Comment'
        db_table = 'feed_comment'


    def __str__(self):
        return f"{self.id}"
