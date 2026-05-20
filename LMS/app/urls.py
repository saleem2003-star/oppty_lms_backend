from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', create_candidate, name='signup'),
    path('signin/', student_sign_in, name='signin   '),
    path('create_course/', create_course, name='create_course'),
    path('get_courses/', get_courses, name='get_courses'),
    
]