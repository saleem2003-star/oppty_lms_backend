from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response    
from rest_framework import status
from .serializers import *
from django.views.decorators.csrf import csrf_exempt




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


@csrf_exempt
@api_view(['GET'])
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


from django.shortcuts import get_object_or_404

@csrf_exempt
@api_view(['GET'])
def get_course_details(request, pk):
    try:
        # Fetch the specific course by its Primary Key (ID)
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    # Fetch related chapters for the curriculum tab
    # chapters = Chapter.objects.filter(course=course)
    # curriculum_list = []
    # for chapter in chapters:
    #     curriculum_list.append({
    #         "title": chapter.title,
    #         "duration": "Video", # You can add a duration field to your Chapter model later if you want real times
    #         "video_url": chapter.video_url
    #     })

    # Prepare the data for the frontend
    course_data = {
        "id": course.id,
        "course_name": course.course_name,
        "price": str(course.price),
        "instructor": course.instructor,
        "thumbnail": course.thumbnail.url if course.thumbnail else None,
        "description": course.description,
        # "curriculum": curriculum_list,
        # If your first chapter has a video, use it as the preview video
        # "video_url": curriculum_list[0]['video_url'] if curriculum_list and curriculum_list[0]['video_url'] else None
    }
    
    return Response(course_data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def enroll_course(request):
    student_id = request.data.get('student_id')
    course_id = request.data.get('course_id')

    if not student_id or not course_id:
        return Response({"error": "student_id and course_id are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the student is already enrolled to prevent duplicates
    if Enrollment.objects.filter(student=student, course=course).exists():
        return Response({"message": "You are already enrolled in this course."}, status=status.HTTP_200_OK)

    # Create the enrollment
    enrollment = Enrollment.objects.create(
        student=student,
        course=course,
        is_active=True  # Set to True so they get immediate access
    )

    return Response({
        "message": "Successfully enrolled!",
        "enrollment_id": enrollment.id
    }, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
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


from django.shortcuts import get_object_or_404
from .models import Enrollment, Chapter

@csrf_exempt
@api_view(['GET'])
def get_my_courses(request, student_id):
    # Fetch all active enrollments for this student
    enrollments = Enrollment.objects.filter(student_id=student_id, is_active=True).select_related('course')
    
    course_list = []
    for enrollment in enrollments:
        course = enrollment.course
        # Count chapters to set the total lessons for the progress bar
        lessons_count = Chapter.objects.filter(course=course).count()
        
        course_list.append({
            "id": course.id,
            "category": "COURSE", # You can update this if you add categories to your model later
            "title": course.course_name,
            "image": course.thumbnail.url if course.thumbnail else "https://via.placeholder.com/800x500?text=No+Thumbnail",
            "authorName": "saleem",
            "authorImg": "https://i.pravatar.cc/150?img=11", # Placeholder instructor image
            # "lessonsCount": lessons_count if lessons_count > 0 else 1 # Prevent division by zero
        })
        
    return Response(course_list, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_course_content(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    # Fetch all chapters for this course
    chapters = Chapter.objects.filter(course=course)
    
    lessons_list = []
    for chapter in chapters:
        lessons_list.append({
            "id": str(chapter.id),
            "title": chapter.title,
            "type": "video" if chapter.video_url else "doc",
            "desc": chapter.content,
            "video_url": chapter.video_url if chapter.video_url else "",
            "notes_url": chapter.notes.url if chapter.notes else ""
        })

    # Structure the response to match the frontend accordion logic
    data = {
        "courseTitle": course.course_name,
        "chapters": [
            {
                "title": "Course Curriculum",
                "lessons": lessons_list
            }
        ]
    }
    
    return Response(data)