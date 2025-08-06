from django.urls import path 
from core.views.index import *
from core.views.account import *


urlpatterns = [
    path('', index_view, name='index_view'),
    path('login', login_view, name='login_view'),
    path('register', register_view, name='register_view'),
]
