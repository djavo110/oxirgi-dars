from django.urls import path, include
from rest_framework.routers import DefaultRouter
from imtihon.views import  StaffRegister, Login, SendOTPView, VerifyOTPView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

from imtihon.views.student_views import ParentsApi, StudentApi
from imtihon.views.teacher_views import TeacherApi, TestApi, CourseApi, DepartmentApi

urlpatterns = [
    path('teacher/', TeacherApi.as_view(), name='teacher'),
    path('course/', CourseApi.as_view(), name='course'),
    path('department/', DepartmentApi.as_view(), name='department'),
    path('student/', StudentApi.as_view(), name='student'),
    path('post/', StaffRegister.as_view(), name='register'),
    path('api/token/', Login.as_view(), name='token_obtain_pair'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('parent/', ParentsApi.as_view(), name='parent'),
    path('test/', TestApi.as_view() , name='test'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]