from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from django.core.validators import FileExtensionValidator 
from utils.models import TimeInfo 
from django.utils import timezone 
from datetime import timedelta 
from tinymce.models  import HTMLField
import os 
from django.dispatch import receiver 


class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email is required!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user 
    

    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeInfo):
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
    )

    nickname = models.CharField(max_length=32, unique=True, null=True, blank=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=110, null=True, blank=True)
    last_name = models.CharField(max_length=110, null=True, blank=True)
    is_verified = models.BooleanField(default=False) # verify by email

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    title = models.CharField(max_length=55, null=True, blank=True,help_text="Ex: Software Engineer")
    gender = models.SmallIntegerField(default=0, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    facebook = models.URLField(max_length=2000, null=True, blank=True)
    x = models.URLField(max_length=2000, null=True, blank=True, help_text='Twitter link')
    # tiktok = models.URLField(max_length=2000, null=True, blank=True)
    instagram = models.URLField(max_length=2000, null=True, blank=True)
    youtube = models.URLField(max_length=2000, null=True, blank=True)
    linkedin = models.URLField(max_length=2000, null=True, blank=True, verbose_name='LinkedIn')
    website = models.URLField(max_length=2000, null=True, blank=True)
    age = models.SmallIntegerField(default=18)
    bio = HTMLField(null=True, blank=True)
    custom_profile = HTMLField(null=True, blank=True)
    avatar = models.FileField(upload_to='profile/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'avif'])])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email if not self.nickname else self.nickname
    

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.fullname = self.first_name + " " + self.last_name
        if not self.fullname:
            if self.first_name and self.last_name:
                self.fullname = self.first_name + " " + self.last_name
            else:
                self.fullname = str(self.email).split('@')[0]
        super(User, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        db_table = 'users'


    @property
    def website_name(self):
        if self.website:
            if self.website.startswith('http://'):
                return self.website[6:].strip('/')
            if self.website.startswith('https://'):
                return self.website[7:].strip('/')
            return self.website.strip('/')
        return ''


    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url 
        return ""


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False 
    
    try:
        old_file = User.objects.get(pk=instance.pk).avatar 
    except User.DoesNotExist:
        return False 
    new_file = instance.avatar 
    try:
        if old_file and old_file.name != new_file.name:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    except Exception as e:
        print(f'Exception delete user avatar on change user avatar: {str(e)}')


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            try:
                os.remove(instance.avatar.path)
            except Exception as e:
                print(f'Exception delete user avatar on delete user avatar: {str(e)}')
