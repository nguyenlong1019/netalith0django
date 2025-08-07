from django.db import models
from utils.models import TimeInfo, SEOBasicAbstract 
from django.utils.text import slugify 
from tinymce.models import HTMLField 


class GroupPage(TimeInfo):
    name = models.CharField(max_length=255, unique=True, verbose_name='Tên group')
    display_in_footer = models.BooleanField(default=False, verbose_name='Hiển thị phần footer?')


    class Meta:
        verbose_name_plural = 'Group Page'
        db_table = 'group_pages'


    def __str__(self):
        return self.name 
    

class PageCategory(TimeInfo):
    name = models.CharField(max_length=255, unique=True, verbose_name='Chủ đề')


    class Meta:
        verbose_name_plural = 'Page Category'
        db_table = 'page_categories'


    def __str__(self):
        return self.name 
    


class StaticPage(TimeInfo, SEOBasicAbstract):
    PAGE_STATUS = (
        (0, 'Draft'),
        (1, 'Delete'),
        (2, 'Publish')
    )

    name = models.CharField(max_length=255, unique=True, verbose_name='Tên trang')
    category = models.ForeignKey(PageCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Chủ đề')
    slug = models.SlugField(max_length=300, null=True, blank=True)
    use_auto_slug = models.BooleanField(default=False)
    group = models.ForeignKey(GroupPage, on_delete=models.SET_NULL, null=True, blank=True)
    content = HTMLField(null=True, blank=True, verbose_name='Nội dung')
    display_status = models.SmallIntegerField(default=2, choices=PAGE_STATUS, verbose_name='Trạng thái hiển thị')


    class Meta:
        verbose_name_plural = 'Static Page'
        db_table = 'static_pages'


    def __str__(self):
        return self.name 
    

    def save(self, *args, **kwargs):
        if not self.slug: # and self.use_auto_slug
            self.slug = slugify(self.name)
        super(StaticPage, self).save(*args, **kwargs)
