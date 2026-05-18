from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', create_candidate, name='signup'),
]