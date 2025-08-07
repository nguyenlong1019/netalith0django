from django.db import models 
from utils.models import TimeInfo 
from tinymce.models import HTMLField 


class AccessLog(TimeInfo):
    page_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    referer = models.TextField(null=True, blank=True)  
    request_path = models.URLField(max_length=2000, null=True, blank=True)
    headers = models.JSONField(null=True, blank=True)
    ip_json = models.JSONField(null=True, blank=True)


    class Meta:
        verbose_name = 'Access Log'
        verbose_name_plural = 'Access Log'
        db_table = 'access_logs'

    
    def __str__(self):
        return f"{self.id} - {self.page_name}"


class EmailLog(TimeInfo):
    action = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255, null=True, blank=True)
    data = HTMLField(null=True, blank=True)
    error = HTMLField(null=True, blank=True)


    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Log'
        db_table = 'email_logs'

    def __str__(self):
        return f"{self.action} - {self.user_email}"