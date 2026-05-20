from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
      


class ActiveUser(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE
    )
    session_key = models.CharField(max_length=255)
    login_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    description = models.TextField()

    def __str__(self):
        return self.course_name



class Enrollment(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True)
    progress = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.expiry_date:
            self.expiry_date = date.today() + relativedelta(months=6)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name}"


class Payment(models.Model):

    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    )
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=200)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )
    payment_method = models.CharField(max_length=50)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    



class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    notes = models.FileField(upload_to='chapter_notes/', blank=True, null=True)

    def __str__(self):
        return f"{self.course.course_name} - {self.title}"
    

