from rest_framework.permissions import BasePermission

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        # faqat teacher bo'lgan userlarga ruxsat beramiz
        return request.user.is_authenticated and getattr(request.user, "role", None) == "teacher"


