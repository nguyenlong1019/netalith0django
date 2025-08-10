from django.urls import path, include 
from core.views.index import *
from core.views.account import *
from core.views.api import *


urlpatterns = [
    path('', index_view, name='index_view'),
    path('login', login_view, name='login_view'),
    path('register', register_view, name='register_view'),
    path('logout', logout_view, name='logout_view'),
    path('verify-email', verify_email_view, name='verify_email_view'),
    path('me', my_profile_view, name='my_profile_view'),
    path('ai0django', ai_assistant_view, name='ai_assistant_view'),
    path('feed/', include([
        path('', feed_view, name='feed_view'),
        path('<category_slug>', feed_category_view, name='feed_category_view'),
        path('<category_slug>/<title_slug>', feed_detail_view, name='feed_detail_view'),
    ])),
    path('post/', include([
        path('', post_view, name='post_view'),
        path('<category_slug>', post_category_view, name='post_category_view'),
        path('<category_slug>/<title_slug>', post_detail_view, name='post_detail_view'),
    ])),
]

urlpatterns += [
    path('api/v1/', include([
        path('auth/refresh', refresh_token_view, name='refresh_token_view'),
        path('ai/ask', ai_ask_api, name='ai_ask_api'),
    ]))
]