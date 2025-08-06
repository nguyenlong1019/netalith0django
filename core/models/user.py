from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from utils.models import TimeInfo 
from django.utils import timezone 
from datetime import timedelta 


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

    fullname = models.CharField(max_length=255, verbose_name='Họ và tên')
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=110, null=True, blank=True, verbose_name='Họ')
    last_name = models.CharField(max_length=110, null=True, blank=True, verbose_name='Tên')
    is_verified = models.BooleanField(default=False) # verify by email

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    gender = models.SmallIntegerField(default=0, choices=GENDER_CHOICES, verbose_name='Giới tính')
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Số điện thoại')
    address = models.TextField(null=True, blank=True, verbose_name='Địa chỉ')
    facebook = models.URLField(max_length=2000, null=True, blank=True)
    zalo = models.URLField(max_length=2000, null=True, blank=True)
    age = models.SmallIntegerField(default=18, verbose_name='Tuổi')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email 
    

    def save(self, *args, **kwargs):
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

