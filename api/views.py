from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from supermarco.models import Student, Course, Teacher, Enrollment
from .serializers import StudentSerializer, CourseSerializer, TeacherSerializer, EnrollmentSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        queryset = Student.objects.all()
        level = self.request.query_params.get('level')
        gender = self.request.query_params.get('gender')
        if level: queryset = queryset.filter(level=level)
        if gender: queryset = queryset.filter(gender=gender)
        return queryset

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        queryset = Teacher.objects.all()
        name = self.request.query_params.get('name')
        if name: queryset = queryset.filter(name__icontains=name)
        return queryset

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def assign_teacher(self, request, pk=None):
        course = self.get_object()
        teacher_id = request.data.get('teacher_id')
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            course.teacher = teacher
            course.save()
            return Response({"status": f"Teacher '{teacher.name}' assigned successfully."})
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll_student(self, request):
        student_id = request.data.get('student_id')
        course_id = request.data.get('course_id')
        try:
            student = Student.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)
        except (Student.DoesNotExist, Course.DoesNotExist):
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        if student.level != course.level:
            return Response({"error": "Levels mismatch"}, status=status.HTTP_400_BAD_REQUEST)

        Enrollment.objects.create(student=student, course=course)
        return Response({"status": "Enrolled successfully."}, status=status.HTTP_201_CREATED)
    
class CustomTokenAuth(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)