from django.contrib import admin
from .models import Relationship, Reply


# Register your models here.
@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    pass


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    pass
# admin.site.register(Reply)
# admin.site.register(Relationship)
