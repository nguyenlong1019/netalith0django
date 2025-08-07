from django.db import models
from utils.models import TimeInfo, SEOBasicAbstract 
from django.dispatch import receiver 
import os 


class SiteInfo(TimeInfo, SEOBasicAbstract):
    brand_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tên thương hiệu')
    site_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Tên trang web')
    site_url = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Link')
    email = models.EmailField(max_length=255, null=True, blank=True, verbose_name='Email')
    hotline = models.CharField(max_length=15, null=True, blank=True, verbose_name='Hotline')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Address')
    zipcode = models.CharField(max_length=31, null=True, blank=True, verbose_name='Zipcode')
    support = models.CharField(max_length=15, null=True, blank=True, verbose_name='Support')
    
    facebook_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Facebook')
    youtube_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Youtube')
    tiktok_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name='Tiktok')
    x_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name='X (Twitter)')
    linkedin_link = models.URLField(max_length=2000, null=True, blank=True, verbose_name='LinkedIn')

    logo = models.ImageField(upload_to='site_imgs/', null=True, blank=True, verbose_name='Logo Image')
    thumb_img = models.ImageField(upload_to='site_imgs', null=True, blank=True, verbose_name='Thumb Image')
    favicon = models.FileField(upload_to='site_imgs', null=True, blank=True, verbose_name='Favicon Icon')

    class Meta:
        ordering = ['site_name', 'email', '-updated_at']
        verbose_name = 'Site Info'
        verbose_name_plural = 'Site Info'
        db_table = 'site_info'

    
    def __str__(self):
        return f"{self.site_name}"
    

    @property 
    def slides_image(self):
        data = list()
        slides = self.homeslide_set.order_by('-updated_at')
        for slide in slides:
            data.append(slide.image_url)
        return data[:3]


@receiver(models.signals.pre_save, sender=SiteInfo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False 
    
    try:
        site_info = SiteInfo.objects.get(pk=instance.pk)
        old_image = site_info.thumb_img 
        old_logo = site_info.logo
        old_fav = site_info.favicon
    except SiteInfo.DoesNotExist:
        return False 
    new_image = instance.thumb_img 
    try:
        if not old_image == new_image:
            if os.path.isfile(old_image.path):
                os.remove(old_image.path)
    except Exception as e:
        print(f'(Site Info)Exception delete thumb image on change thumb image: {str(e)}')

    new_logo = instance.logo 
    try:
        if not old_logo == new_logo:
            if os.path.isfile(old_logo.path):
                os.remove(old_logo.path)
    except Exception as e:
        print(f'(Site Info)Exception delete logo image on change logo image: {str(e)}')

    new_fav = instance.favicon 
    try:
        if not old_fav == new_fav:
            if os.path.isfile(old_fav.path):
                os.remove(old_fav.path)
    except Exception as e:
        print(f'(Site Info)Exception delete Favicon icon on change favicon icon: {str(e)}')


@receiver(models.signals.post_delete, sender=SiteInfo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.thumb_img:
        if os.path.isfile(instance.thumb_img.path):
            try:
                os.remove(instance.thumb_img.path)
            except Exception as e:
                print(f'(Site Info)Exception delete thumb image on delete thumb image: {str(e)}')
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            try:
                os.remove(instance.logo.path)
            except Exception as e:
                print(f'(Site Info)Exception delete logo image on delete logo image: {str(e)}')
    if instance.favicon:
        if os.path.isfile(instance.favicon.path):
            try:
                os.remove(instance.favicon.path)
            except Exception as e:
                print(f'(Site Info)Exception delete favicon icon on delete favicon icon: {str(e)}')


