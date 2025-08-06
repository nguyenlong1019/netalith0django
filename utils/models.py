from django.db import models 
from django.utils.timezone import localtime


class TimeInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-updated_at',)
        abstract = True 


    @property
    def created_at_display(self):
        return localtime(self.created_at).strftime("%d-%m-%Y %H:%M:%S")
    

    @property
    def updated_at_display(self):
        return localtime(self.created_at).strftime("%d-%m-%Y %H:%M:%S")
    

    @property
    def date_published(self):
        return localtime(self.created_at).strftime("%Y-%m-%d")

    @property
    def date_modified(self):
        return localtime(self.updated_at).strftime("%Y-%m-%d")
    

class SEOBasicAbstract(models.Model):
    meta_title = models.CharField(max_length=70, null=True, blank=True)
    meta_description = models.CharField(max_length=160, null=True, blank=True)
    meta_keywords = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        abstract = True 
