#控制后台的显示什么
from django.contrib import admin
from .models import blogtype,blog
# Register your models here.
@admin.register(blogtype)
class blogtypeadmin(admin.ModelAdmin):
	list_display=['id','type_name']

@admin.register(blog)
class blogadmin(admin.ModelAdmin):
	list_display=['id','title','read_num','blog_type','author','Create_time']

'''
@admin.register(Readnum)
class Readnumadmin(admin.ModelAdmin):
	list_display=['read_num','the_blog']
'''