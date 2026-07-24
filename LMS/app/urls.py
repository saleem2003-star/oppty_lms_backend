from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('signup/', create_candidate, name='signup'),
    path('signin/', student_sign_in, name='signin   '),
    path('create_course/', create_course, name='create_course'),
    path('courses/', get_courses, name='get_courses'),
    path('courses/<int:pk>/', get_course_details, name='get_course_details'),
    path('enroll/', enroll_course, name='enroll_course'),
    path('my-courses/<int:student_id>/', get_my_courses, name='get_my_courses'),
    path('course-content/<int:pk>/', get_course_content, name='get_course_content'),
    
]