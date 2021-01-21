from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin

from .models import Relationship, Reply, Message
# 身份验证和权限
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import RelationshipSerializer, RelationshipSetSerializer, ReplySerializer, MessageSerializer


# Create your views here.
class RelationshipViewSet(viewsets.GenericViewSet):
    """
    关系视图集
    """

    def get_queryset(self):
        """
        获取查询集
        :return: 返回特定于用户的项目列表，Relationship关系类中过滤出，
        当前请求中用户的数据
        """
        return Relationship.objects.filter(user=self.request.user)

    def get_permissions(self):
        """
        实例化并返回此视图所需的权限列表,此处设置IsAuthenticated()
        必须登录授权
        :return:
        """
        return [IsAuthenticated()]

    @action(methods="get", detail=False)
    def get_follows(self, request):
        """
        获取关注列表，序列化数据为列表，设定many=True
        state为model设定常量STATE， "1"为关注
        :param request:
        :return:
        """
        follows = Relationship.objects.filter(user=request.user, state="1")
        seria = self.get_serializer(instance=follows, many=True)
        return Response(seria.data)

    @action(methods=["post"], detail=False)
    def set_relation(self, request):
        """
        设定对象关系：删除|修改（关注或屏蔽）|添加（关注或屏蔽）
        :param request: post请求
        :return:尝试设定对对象的关系，user为当前请求的用户，target为Relationship类中设定的target对象
        """
        seria = self.get_serializer(data=request.data)
        seria.is_valid(raise_exception=True)
        try:
            data = Relationship.objects.get(user=request.user, target=seria.validated_data.get("target"))
            if data.state == seria.validated_data.get("state"):
                data.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                data.state = seria.validated_data.get("state")
                data.save()
                # 如果state==1:"关注",需要在消息表中写入关注消息
                if seria.validated_data.get("state") == "1":
                    msg = Message()
                    msg.origin = request.user
                    msg.target = seria.validated_data.get("target")
                    msg.messagetype = "1"
                    msg.save()
                seria = self.get_serializer(instance=data)
                return Response(seria.data)
        except Exception as e:
            seria.save()
            if seria.validated_data.get("state") == "1":
                msg = Message()
                msg.origin = request.user
                msg.target = seria.validated_data.get("target")
                msg.messagetype = "1"
                msg.save()
                # 如果state==1 需要向消息表写入关注信息
            return Response(seria.data)

    def get_serializer(self, *args, **kwargs):
        """
        返回应用于验证和的序列化程序实例
        对输入进行反序列化，并对输出进行序列化。
        :param args:action设置，操作属性在视图上,取决于请求方法。
        :param kwargs:kwargs.setdefault如果key不在字典中，则使用默认值插入key。
        如果key在字典中，则返回key的值，否则为默认值。
        :return:取决于请求方法，返回序列化输出
        """
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == "get_follows":
            return RelationshipSerializer(*args, **kwargs)
        elif self.action == "set_relation":
            return RelationshipSetSerializer(*args, **kwargs)


class ReplyViewSet(viewsets.ModelViewSet):
    """
    回复视图集
    """
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return ReplySerializer(*args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        msg = Message()
        msg.origin = instance.user
        msg.target = instance.diary.diarybook.user
        msg.messagetype = "2"
        msg.reply = instance
        msg.save()


class MessageViewSet(viewsets.GenericViewSet, ListModelMixin):
    """
    消息视图集
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(target=self.request.user)
