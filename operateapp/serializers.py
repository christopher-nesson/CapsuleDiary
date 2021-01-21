from rest_framework import serializers
from .models import Relationship, Message, Reply


class RelationshipSerializer(serializers.ModelSerializer):
    """
    关系序列化类,获取关注列表
    """

    class Meta:
        model = Relationship
        fields = "__all__"


class RelationshipSetSerializer(serializers.ModelSerializer):
    """
    关系设置序列化类，设定对象关系：删除|修改（关注或屏蔽）|添加（关注或屏蔽）
    state：状态
    target：对象
    """

    class Meta:
        model = Relationship
        fields = ["state", "target"]

    def validate(self, attrs):
        """
        fuc校验：自动向属性中添加用户信息，用户不能由前端数据传递
        :param attrs:原数据
        :return:校验后数据
        """
        user = self.context["request"].user
        attrs["user"] = user
        return attrs


class MessageSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = Message
        fields = "__all__"


class ReplySerializer(serializers.ModelSerializer):
    """
    回复序列化类
    exclude:排除
    """

    class Meta:
        model = Reply
        # fields = "__all__"
        exclude = ["user"]

    def validate(self, attrs):
        attrs["user"] = self.context["request"].user
        return attrs
