from django.contrib.auth.backends import ModelBackend
from .models import ProfileUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = ProfileUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except ProfileUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ProfileUser.objects.get(pk=user_id)
        except ProfileUser.DoesNotExist:
            return None
