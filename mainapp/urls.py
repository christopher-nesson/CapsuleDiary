from django.urls import path, include
# 导入views的函数视图
from .views import topics, topic_detail
# 初始版本v1.0基于类的视图
from .views import TopicsView, TopicDetailView
# 进级版本v2.0的视图
from .views import TopicsListCreateMixinGenericAPIView, TopicDetailRetrieveUpdateDestroyView

# 高级版本v3.0的视图
from .views import TopicsListCreateGenericAPIView, TopicDetailRetrieveUpdateDestroyGenericAPIView
# 超级版本v4.0基于基本视图集视图
from .views import TopicViewSet

urlpatterns = [
    # 基于函数的视图(自定义类型)的路由
    # path('topics/', topics),
    # path('topic_detail/<int:id>', topic_detail),
    # 初始版本v1.0基于类的视图(自定义类型)的路由
    # path('topics/', TopicsView.as_view()),
    # path('topic_detail/<int:id>', TopicDetailView.as_view()),
    # 进级版本v2.0的路由
    # path('topics/', TopicsListCreateMixinGenericAPIView.as_view()),
    # path('topic_detail/<int:id>', TopicDetailRetrieveUpdateDestroyView.as_view()),
    # 高级版本v3.0的路由
    # path('topics/', TopicsListCreateGenericAPIView.as_view()),
    # path('topic_detail/<int:id>', TopicDetailRetrieveUpdateDestroyGenericAPIView.as_view()),
    # 超级版本v4.0基于基本视图集视图
    path('topics/', TopicViewSet.as_view(actions={"get": "list", "post": "create"})),
    path('topic_detail/<int:id>', TopicViewSet.as_view(
        actions={"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}))
]
