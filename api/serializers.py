from rest_framework import serializers
from supermarco.models import Student, Course, Teacher, Enrollment

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher_details = TeacherSerializer(source='teacher', read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'hours', 'level', 'teacher', 'teacher_details']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'