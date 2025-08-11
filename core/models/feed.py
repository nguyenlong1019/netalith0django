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
import os 
from django.dispatch import receiver 


PUBLISH_STATUS = (
    (0, 'Draft'),
    (1, 'Published'),
    (2, 'Deleted')
)


class Feed(TimeInfo, SEOBasicAbstract):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=15, default='feed', choices=(('feed', 'Feed'), ('academic', 'Academic')), db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, limit_choices_to={'status': 1}, help_text='Category must be publish status')
    tags = models.ManyToManyField(Tag, help_text='Max 5 tags. If more, extra tags will be truncated.')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, null=True, blank=True)
    content = HTMLField(null=True, blank=True, help_text='For academic type, content must not be empty; if empty, the feed will be saved as Draft.')
    status = models.SmallIntegerField(default=0, choices=PUBLISH_STATUS)
    total_comment = models.IntegerField(default=0)
    total_view = models.IntegerField(default=0)
    total_react = models.IntegerField(default=0)
    banner = models.FileField(upload_to='feed/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])])
    pid = models.CharField(max_length=32, unique=True, default=gen_hex)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    time_reader = models.SmallIntegerField(default=5)

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
    def banner_url(self):
        if self.banner:
            return self.banner.url 
        return ''
    

    @property
    def total_rank(self):
        return self.total_comment + self.total_view + self.total_react 
    

    def save(self, *args, **kwargs):
        self.full_clean()
        
        if not self.slug:
            is_title_exists = Feed.objects.filter(title=self.title).exists()
            if is_title_exists:
                self.slug = slugify(self.title) + "_" + f"{time.time() * 1000}"
            else:
                self.slug = slugify(self.title)
        if self.type == 'academic' and not self.content:
            self.status = 0

        super(Feed, self).save(*args, **kwargs)
        if self.tags.count() > 5:
            self.tags.set(self.tags.all()[:5])


class FeedComment(TimeInfo):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    feed = models.ForeignKey(Feed, null=True, on_delete=models.SET_NULL)
    content = HTMLField()


    class Meta:
        verbose_name_plural = 'Feed Comment'
        db_table = 'feed_comment'


    def __str__(self):
        return f"{self.id}"


@receiver(models.signals.pre_save, sender=Feed)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False 
    
    try:
        old_file = Feed.objects.get(pk=instance.pk).banner 
    except Feed.DoesNotExist:
        return False 
    new_file = instance.banner 
    try:
        if old_file and old_file.name != new_file.name:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Exception as e:
        print(f'Exception delete Feed banner on change Feed banner: {str(e)}')


@receiver(models.signals.post_delete, sender=Feed)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.banner:
        if os.path.isfile(instance.banner.path):
            try:
                os.remove(instance.banner.path)
            except Exception as e:
                print(f'Exception delete Feed banner on delete Feed banner: {str(e)}')
