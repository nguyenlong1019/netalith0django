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
    

class BaseAdmin0Django(admin.ModelAdmin):
    def _is_user0(self, request):
        return (not request.user.is_superuser) and request.user.groups.filter(name='User0Django').exists()


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(status=1)
        # if db_field.name == 'author' and not request.user.is_superuser:
        #     kwargs['queryset'] = User.objects.filter(email=request.user.email)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        field = super().formfield_for_choice_field(db_field, request, **kwargs)
        if db_field.name == "status":
            is_add = request.resolver_match and request.resolver_match.url_name.endswith("_add")
            if is_add:
                field.choices = [(0, "Draft"), (1, "Publish")]
                field.initial = 0
        return field
    

class BaseAdminContent(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if self._is_user0(request):
            ro += ['author']
        return ro
    

    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_superuser:
                obj.author = request.user
        else:
            if not request.user.is_superuser:
                original = type(obj).objects.only('author').get(pk=obj.pk)
                obj.author_id = original.author_id
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAccountAdmin(UserAdmin, BaseAdmin0Django):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User 

    list_display = ['email', 'fullname', 'updated_at_display']
    list_display_links = ['email']
    list_filter = ['is_staff', 'is_superuser', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at',]
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("fullname", "gender", "phone", "address", "facebook", "age")}),
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
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_user0(request):
            return qs.filter(pk=request.user.pk)
        return qs 
    

    def has_view_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        if not self._is_user0(request):
            return super().has_view_permission(request, obj)
        return obj is None or obj.pk == request.user.pk 
    

    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True 
        if not self._is_user0(request):
            return super().has_change_permission(request, obj)
        return obj is None or obj.pk == request.user.pk 


    def get_readonly_fields(self, request, obj = None):
        ro = list(super().get_readonly_fields(request, obj))
        if self._is_user0(request):
            ro += ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'email']        
        return ro 
    

    def get_fieldsets(self, request, obj = None):
        fs = super().get_fieldsets(request, obj)
        if self._is_user0(request):
            fs = tuple(section for section in fs if section[0] != _("Permissions"))
        return fs 
    

    def get_list_filter(self, request):
        if self._is_user0(request):
            return ()  
        return super().get_list_filter(request)


    def get_search_fields(self, request):
        if self._is_user0(request):
            return ()  
        return super().get_search_fields(request)


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
class CategoryAdmin(BaseAdmin0Django):
    search_fields = ['id', 'name',]
    list_display = ['id', 'name', 'updated_at_display',]
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 

    PUBLISHABLE_STATUSES = (0, 1)


    def get_fieldsets(self, request, obj = None):
        if obj is None:
            return (
                (None, {'fields': ('name', 'status')}),
            )
        else:
            if request.user.is_superuser:
                return (
                    (None, {"fields": ("name", "slug", "status")}),
                    ("Dates", {"fields": ("created_at", "updated_at")}),
                    ("Owner", {"fields": ("created_by",)}),
                )
            else:
                return (
                    (None, {"fields": ("name", "status")}),
                    ("Dates", {"fields": ("created_at", "updated_at")}),
                    ("Owner", {"fields": ("created_by",)}),
                )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_user0(request):
            return qs.filter(status__in=self.PUBLISHABLE_STATUSES)
        return qs


    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True 
        if self._is_user0(request):
            if obj is None:
                return True 
            return obj.created_by_id == request.user.id 
        return super().has_change_permission(request, obj)
    

    def get_readonly_fields(self, request, obj=None):
        ro = list(super().get_readonly_fields(request, obj))
        if self._is_user0(request):
            ro += ['created_by']
        return ro
    

    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_superuser:
                obj.created_by = request.user
        else:
            if not request.user.is_superuser:
                original = type(obj).objects.only('created_by').get(pk=obj.pk)
                obj.created_by_id = original.created_by_id
        super().save_model(request, obj, form, change)


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


class BlogCommentStacked(admin.StackedInline):
    model = BlogComment 
    extra = 1


@admin.register(Blog)
class BlogAdmin(BaseAdmin0Django, BaseAdminContent):
    search_fields = ['id', 'title']
    list_display = ['id', 'title', 'updated_at_display']
    list_filter = ['author', 'category', 'created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [BlogCommentStacked]

    fieldsets = (
        ('Edit Blog', {
            'fields': (
                'id', 'title', 'category', 'status', 'content', 'thumb', 'slug', 'total_comment'
            )
        }),
        ("Dates", {"fields": ("created_at", "updated_at")}),
        ("Owner", {"fields": ("author",)}),
        ('SEO Info', {
            'fields': (
                'meta_title', 'meta_description', 'meta_keywords'
            )
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_user0(request):
            return qs.filter(author=request.user)
        return qs
    

    


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    search_fields = ['id', 'blog', 'user']
    list_display = ['id', 'user', 'blog']
    list_filter = ['user', 'blog', 'created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 


class PostCommentStacked(admin.StackedInline):
    model = PostComment 
    extra = 1


@admin.register(Post)
class PostAdmin(BaseAdmin0Django, BaseAdminContent):
    search_fields = ['id', 'author', 'pid']
    list_display = ['id', 'author', 'pid', 'updated_at_display']
    list_filter = ['author', 'category', 'created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 
    inlines = [PostCommentStacked]

    fieldsets = (
        ('Edit Post', {
            'fields': (
                'id', 
                'category', 'status', 'feed', 'total_react', 'total_comment',
            )
        }),
        ("Dates", {"fields": ("created_at", "updated_at")}),
        ("Owner", {"fields": ("author",)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self._is_user0(request):
            return qs.filter(author=request.user)
        return qs


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    search_fields = ['id', 'post', 'user']
    list_display = ['id', 'user', 'post']
    list_filter = ['user', 'post', 'created_at', 'updated_at']
    list_display_links = ['id']
    readonly_fields = ['id', 'created_at', 'updated_at'] 

