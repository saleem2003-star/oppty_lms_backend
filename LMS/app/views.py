from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response    
from rest_framework import status
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@api_view(['POST'])
def student_sign_in(req):
    serializer = Sign_in(data=req.data)
    serializer.is_valid(raise_exception=True)
    student = serializer.validated_data['student']
    return Response({
        "message": "success",
        "id": student.id,
        "name": student.name,
        "email": student .email

    }, status=status.HTTP_200_OK)
    


@csrf_exempt
@api_view(['POST'])
def create_candidate(req):
    serializer = Create_Candidate(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def get_courses(req):
    courses = Course.objects.all()
    course_list = []
    for course in courses:
        course_list.append({
            "id": course.id,
            "course_name": course.course_name,
            "price": course.price,
            "instructor": course.instructor,
            "thumbnail": course.thumbnail.url if course.thumbnail else None,
            "description": course.description
        })
    return Response(course_list, status=status.HTTP_200_OK)

def create_course(req):
    course_name = req.data.get('course_name')
    price = req.data.get('price')
    instructor = req.data.get('instructor')
    thumbnail = req.FILES.get('thumbnail')
    description = req.data.get('description')

    course = Course.objects.create(
        course_name=course_name,
        price=price,
        instructor=instructor,
        thumbnail=thumbnail,
        description=description
    )
    return Response({
        "id": course.id,
        "course_name": course.course_name,
        "price": course.price,
        "instructor": course.instructor,
        "thumbnail": course.thumbnail.url if course.thumbnail else None,
        "description": course.description
    }, status=status.HTTP_201_CREATED)


