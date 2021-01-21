from django.db import models
from userapp.models import CustomUser
from mainapp.models import Diary

STATE = (
    ("1", "关注"),
    ("2", "屏蔽"),
)


# Create your models here.
class Relationship(models.Model):
    """
    关系类，用户可以关注或屏蔽其他用户对象
    在一个模型中，如果有多个字段的外键是同一张表，需要使用到related_name；
    使用related_name之后不能按照以往的user.relationship_set.all()一找多，应该使用user.relations.all()
    """
    user = models.ForeignKey(CustomUser, related_name="relations", on_delete=models.CASCADE, verbose_name="用户")
    target = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="对象")
    state = models.CharField(max_length=1, choices=STATE, verbose_name="状态")

    def __str__(self):
        return "用户" + self.user.username + STATE[int(self.state) - 1][1] + self.target.username

    class Meta:
        unique_together = ["user", "target"]


class Reply(models.Model):
    """
    回复类，日记下的回复
    """
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, verbose_name="所属日记")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="所属用户")
    info = models.CharField(max_length=100, verbose_name="回复内容")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="回复时间")

    def __str__(self):
        return self.info


MESSAGETYPE = (
    ("1", "关注"),
    ("2", "回复"),
)


class Message(models.Model):
    """
    消息类
    """
    origin = models.ForeignKey(CustomUser, related_name="msgs", on_delete=models.CASCADE, verbose_name="消息源")
    target = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="消息接受者")
    messagetype = models.CharField(max_length=1, choices=MESSAGETYPE, verbose_name="消息类型")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    reply = models.ForeignKey(Reply, null=True, blank=True, on_delete=models.CASCADE, verbose_name="所属回复")

    def __str__(self):
        return self.origin.username + "的消息"
