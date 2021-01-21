from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializers, CustomUserRegistSerializers, CustomUserHeadPicSerializers, \
    CustomUserPasswordSerializers


# class CustomUserViewSets(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#
#     # serializer_class = CustomUserSerializers
#     def get_serializer(self, *args, **kwargs):
#         if self.action == "create":
#             return CustomUserRegistSerializers(*args, **kwargs)
#         else:
#             return CustomUserSerializers()
#
#     @action(methods=["patch"], detail=True)
#     def setheadpic(self, request, pk):
#         try:
#             user = CustomUser.objects.get(id=pk)
#         except(TypeError, KeyError):
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         seria = CustomUserHeadPicSerializers(data=request.data)
#         if seria.is_valid():
#             user.headpic = seria.validated_data.get("headpic")
#             seria.save()
#             seria2 = CustomUserSerializers(user)
#             return Response(seria2.data)
#         else:
#             return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=["patch"], detail=True)
#     def setpassword(self, request, pk):
#         try:
#             user = CustomUser.objects.get(id=pk)
#         except(TypeError, KeyError):
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         seria = CustomUserPasswordSerializers(data=request.data)
#         if seria.is_valid():
#             if user.check_password(seria.validated_data.get("passwordold")):
#                 user.check_password(seria.validated_data.get("passwordnew"))
#                 user.save()
#                 seria2 = CustomUserSerializers(user)
#                 return Response(seria2.data)
#             else:
#                 return Response("原始密码错误")
#         else:
#             return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSets(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()

    # serializer_class = CustomUserSerializers

    def get_permissions(self):
        if self.action in ["setheadpic", "setpassword", "getuserinfo"]:
            return [IsAuthenticated()]
        else:
            return []

    def get_serializer(self, *args, **kwargs):
        """
        重写父类中获取序列化类需要 给context赋值
        :param args:
        :param kwargs:
        :return:
        """
        # 确保能够初始化context
        kwargs.setdefault('context', self.get_serializer_context())
        if self.action == "create":
            return CustomUserRegistSerializers(*args, **kwargs)
        elif self.action == "setheadpic":
            return CustomUserHeadPicSerializers(*args, **kwargs)
        elif self.action == "setpassword":
            return CustomUserPasswordSerializers(*args, **kwargs)
        elif self.action == "getuserinfo":
            return CustomUserSerializers(*args, **kwargs)

    @action(methods=["get"], detail=False)
    def getuserinfo(self, request):
        seria = CustomUserSerializers(instance=request.user)
        return Response(seria.data)

    @action(methods=["patch"], detail=False)
    def setheadpic(self, request, *args, **kwargs):
        seria = self.get_serializer(data=request.data, *args, **kwargs)
        seria.is_valid(raise_exception=True)
        request.user.headpic = seria.validated_data.get("headpic")
        request.user.save()
        seria2 = CustomUserSerializers(instance=request.user)
        return Response(seria2.data)

    @action(methods=["patch"], detail=False)
    def setpassword(self, request, *args, **kwargs):
        seria = self.get_serializer(data=request.data, *args, **kwargs)
        seria.is_valid(raise_exception=True)
        request.user.set_password(seria.validated_data.get("passwordnew"))
        request.user.save()
        seria2 = CustomUserSerializers(instance=request.user)
        return Response(seria2.data)
