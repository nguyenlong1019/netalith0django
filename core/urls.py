from django.urls import path, include 
from core.views.index import *
from core.views.account import *


urlpatterns = [
    path('', index_view, name='index_view'),
    path('login', login_view, name='login_view'),
    path('register', register_view, name='register_view'),
    path('logout', logout_view, name='logout_view'),
    path('verify-email', verify_email_view, name='verify_email_view'),
    path('me', my_profile_view, name='my_profile_view'),
]

urlpatterns += [
    path('api/', include([
        path('auth/refresh', refresh_token_view, name='refresh_token_view'),
    ]))
]