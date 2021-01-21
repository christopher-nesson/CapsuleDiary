from django.contrib import admin
from .models import Topic, DayBook, Diary, ImageDiary


# Register your models here.
# 注册模型类到Django的API后台管理界面
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(DayBook)
class DayBookAdmin(admin.ModelAdmin):
    pass


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageDiary)
class ImageDiaryAdmin(admin.ModelAdmin):
    pass
