"""CapsuleDiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from .settings import MEDIA_ROOT
# 获取刷新验证JWT
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify

# 使用DRF注册资源，生成对应资源的路由
from rest_framework.routers import DefaultRouter
from mainapp.views import TopicViewSets, DayBookViewSets, DiaryViewSets, ImageDiaryViewSets
from userapp.views import CustomUserViewSets
from operateapp.views import RelationshipViewSet, ReplyViewSet,MessageViewSet

# 终极版本v4.0路由注册方式
router = DefaultRouter()
# router.register("topics", TopicViewSets)
# 终极版本函数路由注册方式,注册多出必填参数basename，
# 约定为注册资源的小写即model类里边的模型类名小写
router.register("topics", TopicViewSets, basename="topic")
router.register("customusers", CustomUserViewSets, basename="customuser")
# router.register("daybooks", DayBookViewSets)
router.register("daybooks", DayBookViewSets, basename="daybook")
# router.register("diarys", DiaryViewSets)
router.register("diarys", DiaryViewSets, basename="diary")
router.register("imagediarys", ImageDiaryViewSets, basename="imagediary")
router.register("relationships", RelationshipViewSet, basename="relationship")
router.register("replys", ReplyViewSet, basename="reply")
router.register("messages", MessageViewSet, basename="message")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # 终极版本v4.0路由
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 测试视图进化版本的路由，写在mainapp中
    # path('', include(("mainapp.urls", "mainapp"))),
    # JWT路由用于获取token的路由obtain
    path('obtainjwt/', token_obtain_pair),
    # JWT路由用于刷新token的路由refresh
    path('refreshjwt/', token_refresh),
    # JWT路由用于验证token的路由verify
    path('verifyjwt/', token_verify),

]
