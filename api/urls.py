from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
path('token-auth/', views.CustomTokenAuth.as_view(), name='api_token_auth'),]