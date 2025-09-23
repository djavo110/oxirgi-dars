from django.urls import path, include
from rest_framework.routers import DefaultRouter
from imtihon.views import  AdminCreateStudent, ChangePassword, Login, SendOTPView, VerifyOTP
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

from imtihon.views.student_views import ParentsApi, StudentApi
from imtihon.views.teacher_views import TeacherApi, TestApi, CourseApi, DepartmentApi
from imtihon.views.group_views import *

router = DefaultRouter()
router.register(r'days', DayViewSet)
router.register(r'rooms', RoomsViewSet)
router.register(r'table-types', TableTypeViewSet)
router.register(r'tables', TableViewSet)
router.register(r'group-students', GroupStudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('teacher/', TeacherApi.as_view(), name='teacher'),
    path('course/', CourseApi.as_view(), name='course'),
    path('department/', DepartmentApi.as_view(), name='department'),
    path('student/', StudentApi.as_view(), name='student'),
    path('admin-created/', AdminCreateStudent.as_view(), name='admin'),
    path('change-password/', ChangePassword.as_view(), name='change_password'),
    path('api/token/', Login.as_view(), name='token_obtain_pair'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('parent/', ParentsApi.as_view(), name='parent'),
    path('test/', TestApi.as_view() , name='test'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]