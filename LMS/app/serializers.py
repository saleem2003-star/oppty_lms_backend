from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *

class Sign_in(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        try:
            student=Student.objects.get(email=email,password=password)
        except:
            raise ValidationError("INVALID EMAIL OR PASSWORD")
        data['student']=student
        return data
    
class Create_Candidate(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
        


class Admin_Sign_in(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    def validate(self,data):
        email=data.get('email')
        password=data.get('password')
        try:
            admin=Admin.objects.get(email=email,password=password)
        except:
            raise ValidationError("INVALID EMAIL OR PASSWORD")
        data['admin']=admin
        return data
    