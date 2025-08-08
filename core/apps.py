from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'


    # def ready(self):
    #     super().ready()
    #     from django.db.models.signals import post_migrate 
    #     from django.contrib.auth.models import Group 


    #     def ensure_groups(sender, **kwargs):
    #         Group.objects.get_or_create(name="User0Django")
        
    #     post_migrate.connect(ensure_groups, dispatch_uid="ensure_groups_core")
