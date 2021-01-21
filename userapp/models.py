from django.db import models
from django.contrib.auth.models import AbstractUser

STATE = (
    ("0", "上榜"),
    ("1", "不上榜"),
)


# Create your models here.
class CustomUser(AbstractUser):
    """
    继承Django自带的用户基类，扩展自定义属性
    """
    email = models.EmailField(unique=True, verbose_name="邮箱")
    headpic = models.ImageField(upload_to="user/", default="user/default.png", verbose_name="用户头像"
                                )
    telephone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")
    onlist = models.CharField(choices=STATE, max_length=1, verbose_name="是否上榜", default="0")
    self_introduction = models.CharField(max_length=60, null=True, blank=True, verbose_name="自我介绍")

