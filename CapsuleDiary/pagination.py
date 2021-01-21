"""
Master:Chao
Datetime:2021/1/14 16:13
Reversion:1.0
File: pagination.py
继承DRF中的分页类，配置默认使用的全局分页类,BasePagination为分页类的基类，
PageNumberPagination一个简单的基于页码的样式，支持页码查询参数
LimitOffsetPagination基于limit限制/offset偏移量的样式
"""
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class SuperPageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"

# class SuperLimitOffsetPagination(LimitOffsetPagination):
#     limit_query_param = "superlimit"
#     offset_query_param = "superoffset"
