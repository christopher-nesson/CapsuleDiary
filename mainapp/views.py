"""建立模型对应的视图集
模型视图集 ModelViewSet
基于函数的视图
基于类(APIView)的视图
基于基本类(GenericAPIView)的视图
基于混合类的视图(generic.*, mixins.*)
基于混合基本类的视图(generic.*)
基于视图集和自定义路由  在as_view中需要使用action 将http动词 与操作绑定
基于视图集与默认基本路由   通过router.register() 自动生成路由"""

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import View
from rest_framework.views import APIView

from .models import Topic, DayBook, Diary, ImageDiary
from .serializers import TopicSerializers, DayBookSerializers, DiarySerializers, ImageDiarySerializers
from django.http import HttpResponseNotAllowed

# 身份验证和权限
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# 扩展的认证类
from CapsuleDiary.permissions import IsSuperAdminUser
from CapsuleDiary.authentication import NoCsrfSessionAuthentication
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication


# 最终版本，基于rest_framework的模型视图集的视图，
# 由rest_framework封装好的模型视图，安全便捷，最好用，但由于封装度过高，不利于改写
# 可以通过复写自定义函数来扩展和修改继承类的功能queryset:查询集合 serializer_class:序列化类
class TopicViewSets(viewsets.ModelViewSet):
    """
    话题的视图集
    """
    from django_filters.rest_framework import DjangoFilterBackend
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['create_time', 'id']
    search_fields = ['info', 'img']
    ordering_fields = ['create_time', 'id']

    # queryset = Topic.objects.all()
    def get_queryset(self):
        return Topic.objects.all()

    # serializer_class = TopicSerializers
    def get_serializer(self, *args, **kwargs):
        return TopicSerializers(*args, **kwargs)

    # 默认的身份验证类
    # authentication_classes = [BasicAuthentication]
    def get_authenticators(self):
        return [BasicAuthentication(), NoCsrfSessionAuthentication(), JWTAuthentication()]

    # 默认许可类
    # permission_classes = [IsAdminUser]
    def get_permissions(self):
        """
        如果请求的方式是current函数中的，返回普通用户GET(list)到的当天的话题
        elif 的请求为 PUT(update) PATCH(partial_update)修改话题 GET(retrieve获得指定id的话题)，为普通管理员的权限范围
        else 的请求诶 POST(create) DEL(destroy) 为超级管理员的权限，只有其才能增加和删除
        :return: 权限 AllowAny:所有人  IsAdminUser:管理员  IsSuperAdminUser:超级管理员
        """
        if self.action == "current":
            return [AllowAny()]
        elif self.action == "create_topic_diary":
            return [IsAuthenticated()]
        elif self.action == "update" or self.action == "partial_update" or self.action == "retrieve" or \
                self.action == "list":
            return [IsAdminUser()]
        else:
            return [IsSuperAdminUser()]

    """
    detail 代表是列表路由后拼接  或者是详情路由后拼接
    detail False /topics/current
    detail True  /topics/101/current
    """

    @action(methods=["get"], detail=False)
    def current(self, request):
        """
        普通用户的get请求只能获得当天的话题，即创建时间最新的话题排序最后的话题
        :param request: 请求
        :return: 响应(序列化后的数据)
        """
        t = Topic.objects.last()
        seria = self.get_serializer(t)
        return Response(seria.data)
        # /topics/1/create_topic_diary

    @action(methods=["post"], detail=True)
    def create_topic_diary(self, request, pk):
        try:
            topic = Topic.objects.get(id=int(pk))
        except(TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 需要跟model字段保持一致，在postman中请求也一致
        if request.FILES.get("image"):
            seria = ImageDiarySerializers(data=request.data)
            if seria.is_valid():
                instance = seria.save()
                instance.topic = topic
                instance.save()
                return Response(seria.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            seria = DiarySerializers(data=request.data)
            if seria.is_valid():
                instance = seria.save()
                instance.topic = topic
                instance.save()
                return Response(seria.data, status=status.HTTP_201_CREATED)
            else:
                return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)


class DayBookViewSets(viewsets.ModelViewSet):
    """
    日记本视图集
    """

    # queryset = DayBook.objects.all()
    def get_queryset(self):
        """
        用户的查询集必须为自己的日记本列表
        超级管理员可看所有人的日记列表
        :return:
        """
        if self.request.user.is_superuser:
            return DayBook.objects.all()
        else:
            return DayBook.objects.filter(user=self.request.user)

    serializer_class = DayBookSerializers

    def get_permissions(self):
        """
        请求为 PUT(update) PATCH(partial_update)：修改 GET(list)GET(retrieve获得指定)：获得列表或指定单个
        的请求诶 POST(create)：创建 DEL(destroy)：删除
        :return:只允许通过身份验证的用户访问为IsAuthenticated的实例。
        """
        if self.action in ["create", "list", "partial_update", "retrieve", "update", "destroy"]:
            return [IsAuthenticated()]
        else:
            return []

    @action(detail=True)
    def get_diarys(self, request, pk):
        try:
            daybook = DayBook.objects.get(id=int(pk))
            seria = DiarySerializers(instance=daybook.diary_set.all(), many=True)
            return Response(seria.data)
        except (TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)


from CapsuleDiary.pagination import SuperPageNumberPagination


class DiaryViewSets(viewsets.GenericViewSet, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin,
                    ListModelMixin):
    """
    日记视图集
    """

    queryset = Diary.objects.all()
    serializer_class = DiarySerializers

    def get_permissions(self):
        if self.action in ["create", "partial_update", "retrieve", "update", "destroy"]:
            return [IsAuthenticated()]
        else:
            return []

    @action(methods=["get"], detail=False, pagination_class=SuperPageNumberPagination)
    def get_latest(self, request, **kwargs, ):
        from datetime import date
        diarys = Diary.objects.filter(create_time__date=date.today()).order_by("-create_time")

        if self.paginator:
            # 分页过的最新日记
            paged_diarys = self.paginate_queryset(diarys)
            seria = DiarySerializers(instance=paged_diarys, many=True)
            paged_seriadata = self.get_paginated_response(seria.data)
            return paged_seriadata
        else:
            seria = DiarySerializers(instance=diarys, many=True)
            return Response(seria.data)


class ImageDiaryViewSets(viewsets.GenericViewSet, CreateModelMixin, DestroyModelMixin, UpdateModelMixin,
                         RetrieveModelMixin):
    """
    图片日记视图集
    """
    queryset = ImageDiary.objects.all()
    serializer_class = ImageDiarySerializers

    def get_permissions(self):
        if self.action in ["create", "destroy", "partial_update", "retrieve", "update"]:
            return [IsAuthenticated()]
        else:
            return []


# 基于函数的视图(自定义类型)，研究rest_framework封装原理的自定义函数视图
# from django.http import HttpResponseNotAllowed


# Django中的请求和响应
# DRF中的请求和响应实质是对Django中请求响应进行封装
# 使用装饰器将Django封装的请求转换为DRF中的请求
# from rest_framework.decorators import api_view

# 使用装饰器将Django封装的响应转换为DRF中的响应
# from rest_framework.response import Response
# 导入状态码
# from rest_framework import status


@api_view(http_method_names=['GET', 'POST'])
def topics(req):
    if req.method == 'GET':
        ts = Topic.objects.all()
        # 获取的seria是个列表所以参数设置为many=True
        seria = TopicSerializers(instance=ts, many=True)
        return Response(seria.data)
    elif req.method == 'POST':
        seria = TopicSerializers(data=req.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET', 'PUT', 'PATCH', 'DELETE'])
def topic_detail(req, id):
    try:
        t = Topic.objects.get(id=id)
    except(TypeError, KeyError):
        return Response(status=status.HTTP_404_NOT_FOUND)
    if req.method == 'GET':
        seria = TopicSerializers(t)
        return Response(seria.data)
    elif req.method == 'PUT' or req.method == 'PATCH':
        seria = TopicSerializers(instance=t, data=req.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif req.method == 'DELETE':
        t.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'PATCH', 'DELETE'])


# 基于类的视图(自定义类型)，研究rest_framework封装原理的自定义类视图
# from django.views.generic import View


class MyView(View):
    """
    示例类，将函数写在类中
    """

    def get(self, request):
        pass

    def post(self, request):
        pass


# 初始版本v1.0从rest_framework视图中导入并继承APIView，创建自定义视图
# from rest_framework.views import APIView


class TopicsView(APIView):
    @staticmethod
    def get(request):
        topics: Topic = Topic.objects.all()
        # 获取的seria是个列表所以参数设置为many=True
        seria = TopicSerializers(topics, many=True)
        return Response(seria.data)

    @staticmethod
    def post(request):
        seria = TopicSerializers(data=request.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TopicDetailView(APIView):
    @staticmethod
    def get(request, id):
        try:
            t = Topic.objects.get(id=id)
        except(TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        seria = TopicSerializers(instance=t)
        return Response(seria.data)

    @staticmethod
    def put(request, id):
        try:
            t = Topic.objects.get(id=id)
        except(TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        seria = TopicSerializers(instance=t, data=request.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def patch(request, id):
        try:
            t = Topic.objects.get(id=id)
        except (TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        seria = TopicSerializers(instance=t, data=request.data)
        if seria.is_valid():
            seria.save()
            return Response(seria.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, id):
        try:
            t = Topic.objects.get(id=id)
            t.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except(TypeError, KeyError):
            return Response(status=status.HTTP_404_NOT_FOUND)


# 进级版本v2.0从rest_framework视图中导入继承APIView的GenericAPIView，
# 和mixins中的ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin来创建自定义视图
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
#     DestroyModelMixin


class TopicsListCreateMixinGenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TopicDetailRetrieveUpdateDestroyView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin,
                                           DestroyModelMixin):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# 高级版本v3.0
# 从Generic中导入继承ListModelMixin,CreateModelMixin,GenericAPIView的ListCreateAPIView
# 以及继承GenericAPIView，RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin的RetrieveUpdateDestroyAPIView来创建自定义视图
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class TopicsListCreateGenericAPIView(ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers


class TopicDetailRetrieveUpdateDestroyGenericAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers


# 超级版本v4.0基于基本视图集合GenericViewSet创建视图
# from rest_framework.viewsets import GenericViewSet

class TopicViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,
                   DestroyModelMixin):
    lookup_field = "id"
    queryset = Topic.objects.all()
    serializer_class = TopicSerializers
