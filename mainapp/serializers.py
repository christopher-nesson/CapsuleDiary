"""
Master:Chao
Datetime:2021/1/6 19:35
Reversion:1.0
File: serializers.py
"""
# 新建模型的序列化类，指明序列化的方式
from rest_framework import serializers
from .models import Topic, DayBook, Diary, ImageDiary


class TopicSerializers(serializers.ModelSerializer):
    """
        指明模型类的序列化方式 model指明模型  fields指明待序列化的字段
    """

    class Meta:
        model = Topic
        fields = "__all__"


class DayBookSerializers(serializers.ModelSerializer):
    """
    指明模型类的序列化方式 model:指明模型 fields:指明待序列化的字段
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DayBook
        fields = ["id", "user", "motif", "describe", "img", "create_time", "expiration_time", "jurisdiction"]

    def validate(self, attrs):
        """
        fuc校验：自动向属性中添加用户信息，用户不能由前端数据传递
        :param attrs:
        :return:
        """
        attrs["user"] = self.context["request"].user
        return attrs

    def validate_motif(self, value):
        """
        fuc检验：用户与日记标题唯一
        :param value:
        :return:
        """
        if DayBook.objects.filter(user=self.context["request"].user, motif=value).exists():
            raise serializers.ValidationError("已创建该日记本")
        else:
            return value

    @staticmethod
    def validate_expiration_time(value):
        """
        fuc检验：过期时期不能早于创建日期
        :param value:
        :return:
        """
        from datetime import date
        if value > date.today():
            return value
        else:
            raise serializers.ValidationError("过期时间有误，需晚于创建时间")


class DiarySerializers(serializers.ModelSerializer):
    """
    展示日记本相关内容：
    1、主键展示,主键默认id
    2、model模型类中def __str__函数展示
    3、展示任意字段，slug_field = 需要展示的model类中需要展示的字段
    4、展示外键的超链接地址
    5、展示外键模型类的所有字段
    """
    # daybook = serializers.PrimaryKeyRelatedField(read_only=True)
    # daybook = serializers.StringRelatedField()
    daybook = serializers.SlugRelatedField(slug_field="motif", read_only=True)
    # daybook = serializers.HyperlinkedRelatedField(view_name="daybook-detail", read_only=True)

    # daybook = DayBookSerializers()

    class Meta:
        model = Diary
        # fields = "__all__"
        fields = ["id", "daybook", "topic", "content", "create_time", "importance"]

    def validate(self, attrs):
        return attrs


class ImageDiarySerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageDiary
        fields = "__all__"
