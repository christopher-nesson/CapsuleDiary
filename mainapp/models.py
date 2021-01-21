from django.db import models
from userapp.models import CustomUser

STATE = (
    ("0", "所有人可见"),
    ("1", "仅自己可见"),

)


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=30, verbose_name="话题标题")
    img = models.ImageField(upload_to="topic/", default="topic/default.png", verbose_name="话题配图")
    info = models.CharField(max_length=100, null=True, blank=True, verbose_name="话题描述")
    create_time = models.DateField(auto_now_add=True, verbose_name="发布时间")

    def __str__(self):
        return self.title


class DayBook(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="所属用户")
    motif = models.CharField(max_length=30, verbose_name="日记本主题")
    describe = models.CharField(max_length=200, null=True, blank=True, verbose_name="日记本描述")
    img = models.ImageField(upload_to="cover/", null=True, blank=True, verbose_name="封面")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    expiration_time = models.DateField(verbose_name="过期时间")
    jurisdiction = models.CharField(max_length=1, choices=STATE, verbose_name="可见管理", default="0")

    def __str__(self):
        return self.user.username + "的日记本:" + self.motif

    class Meta:
        unique_together = ["user", "motif"]


class Diary(models.Model):
    daybook = models.ForeignKey(DayBook, on_delete=models.CASCADE, verbose_name="所属日记本")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, verbose_name="话题", null=True, blank=True)
    content = models.TextField(verbose_name="日记内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    importance = models.BooleanField(default=False, verbose_name="重要日记")

    def __str__(self):
        return self.content[:20]


class ImageDiary(Diary):
    image = models.ImageField(upload_to="imagediary/", verbose_name="配图")
