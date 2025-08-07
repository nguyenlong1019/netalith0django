from django.contrib import admin
from core.models.log import AccessLog, EmailLog 
from core.models.user import User 
from django.contrib.contenttypes.models import ContentType 
from django.contrib.sessions.models import Session 
from django.contrib.admin.models import LogEntry 
from django.contrib.auth.admin import UserAdmin 
from django.utils.translation import gettext_lazy as _
from utils.utils import to_localdate 
from core.models.site_info import SiteInfo 
from core.models.category import Category 
from core.models.page import StaticPage, PageCategory, GroupPage 
from core.models.blog import Blog, BlogComment
from core.models.post import Post, PostComment 
from core.forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    search_fields = ['id', 'model']
    list_display = ['id', 'app_label', 'model']
    list_filter = ['app_label']
    
    def get_model_perms(self, request):
        self.model._meta.verbose_name = 'Loại nội dung'
        self.model._meta.verbose_name_plural = 'Loại nội dung'
        return super().get_model_perms(request)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date_formatted']

    def get_readonly_fields(self, request, obj = ...):
        return [field.name for field in self.model._meta.get_fields()]

    
    def get_model_perms(self, request):
        self.model._meta.verbose_name = 'Phiên làm việc'
        self.model._meta.verbose_name_plural = 'Phiên làm việc'
        return super().get_model_perms(request)

    @admin.display(description='Expire date')
    def expire_date_formatted(self, obj):
        return to_localdate(obj.expire_date)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user']
    list_display = ['id', 'user', 'action_flag', 'change_message']
    list_filter = ['user']
    ordering = ['-action_time']

    def get_readonly_fields(self, request, obj = ...):
        return [field.name for field in self.model._meta.get_fields()]


    def get_model_perms(self, request):
        self.model._meta.verbose_name = 'Action Log'
        self.model._meta.verbose_name_plural = 'Action Log'
        return super().get_model_perms(request)


@admin.register(User)
class UserAccountAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User 

    list_display = ['email', 'fullname', 'updated_at_display']
    list_display_links = ['email']
    list_filter = ['is_staff', 'is_superuser', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at',]
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("fullname", "gender", "phone", "address", "facebook", "zalo", "age")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff",
                                       "is_superuser", "groups",
                                       "user_permissions")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "fullname",
                       "password1", "password2",
                       "is_staff", "is_superuser"),
        }),
    )
    
    search_fields = ('id', 'email',)
    ordering = ['-updated_at']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    search_fields = ['id', 'user_email',]
    list_display = ['id', 'user_email', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    search_fields = ['id', 'ip_address', 'user_agent']
    list_display = ['id', 'page_name', 'ip_address', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at', 'page_name', 'country']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    search_fields = ['site_name']
    list_display = ['email', 'site_name', 'updated_at_display']
    list_filter = ['created_at', 'updated_at']
    list_editable = ['site_name']
    list_display_links = ['email']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = (
        ('Edit Site', {
            'fields': (
                'id', 'created_at', 'updated_at',
                'logo', 'thumb_img', 'favicon', 'brand_name',
                'site_name', 'site_url',
            )
        }),
        ('Edit Contact', {
            'fields': (
                'address', 'email', 'hotline', 'zipcode', 'support',
            )
        }),
        ('Edit Socials', {
            'fields': (
                'facebook_link', 'youtube_link', 'tiktok_link', 'x_link', 'linkedin_link'
            )
        }),
        ('Edit SEO Info', {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords'
            )
        })
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]
    list_display = ['id', 'name', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


@admin.register(PageCategory)
class PageCategoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]
    list_display = ['id', 'name', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


@admin.register(GroupPage)
class GroupPageAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]
    list_display = ['id', 'name', 'display_in_footer', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]
    list_display = ['id', 'name', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass 


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    pass 


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass 


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass 
