from django.db import models 
from utils.models import TimeInfo 
from tinymce.models import HTMLField
from .user import User 


class AssistantLog(TimeInfo):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_msg = models.TextField(null=True, blank=True)
    assistant_msg = models.TextField(null=True, blank=True)
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    cid = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Assistant Log'
        db_table = 'assistants'
    

    def __str__(self):
        return self.cid 
