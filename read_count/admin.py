from django.contrib import admin
from .models import Readnum,Readnum_detail
# Register your models here.

@admin.register(Readnum)
class Readnumadmin(admin.ModelAdmin):
	list_display=['read_num','content_object']


@admin.register(Readnum_detail)
class Readnum_detailadmin(admin.ModelAdmin):
	list_display=['read_num','date','content_object']