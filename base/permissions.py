from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import *

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('pk', None)
        if user_id:
            user = CustomUser.objects.filter(id=user_id).first()
            if not user.is_verified:
                raise PermissionDenied('this account is not verified')
            return True
        else:
            user_ = request.user.id
            user = CustomUser.objects.filter(id=user_).first()
            if not user.is_verified:
                raise PermissionDenied('this account is not verified')
            return True

class PermissionResetPassword(BasePermission):
    def has_permission(self, request, view):
        user_id = request.pk
        code_verification = CodeVerification.objects.filter(user__id=user_id).first()
        if not code_verification.is_verified:
            raise PermissionDenied("ليس لديك الصلاحية بتغيير كلمة المرور")
        return True

class HaveCodeVerifecation(BasePermission):
    def has_permission(self, request, view):
        user_id = request.pk
        code_verification = CodeVerification.objects.filter(user__id=user_id).first()
        if not code_verification:
            raise PermissionDenied("الرجاء طلب رمز التحقق والمحاولة من جديد")
        return True