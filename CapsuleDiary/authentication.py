"""
Master:Chao
Datetime:2021/1/8 14:09
Reversion:1.0
File: authentication.py
"""
from rest_framework.authentication import SessionAuthentication


class NoCsrfSessionAuthentication(SessionAuthentication):
    """
    扩展DRF自带的session认证类，不需要csrf跨站请求认证
    """

    def enforce_csrf(self, request):
        return True
