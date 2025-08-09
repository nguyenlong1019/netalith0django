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
]

urlpatterns += [
    path('api/v1/', include([
        path('auth/refresh', refresh_token_view, name='refresh_token_view'),
        path('ai/ask', ai_ask_api, name='ai_ask_api'),
    ]))
]