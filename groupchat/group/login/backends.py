from ..models import RegisteredUsers
from django.contrib.auth.hashers import check_password


class CustomAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        user = RegisteredUsers.objects.filter(email=username)
        if user:
            if check_password(password, user[0].password):
                return user[0]
            else:
                return None
        else:
            return None

    def get_user(self, user_id):
        user = RegisteredUsers.objects.filter(id=user_id)
        if not user:
            return None
        return user[0]


