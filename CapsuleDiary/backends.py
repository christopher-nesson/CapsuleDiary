"""
Master:Chao
Datetime:2021/1/12 9:53
Reversion:1.0
File: backends.py
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# get_user_model()返回此项目中激活的用户模型
UserModel = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get("email")
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(email=username)
        except UserModel.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
