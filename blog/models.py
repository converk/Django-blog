from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField   #导入富文本编辑
from django.contrib.contenttypes.models import ContentType
from read_count.models import Readnum,Readnum_extand

# Create your models here.


class blogtype(models.Model):  #设置博客类型
    type_name=models.CharField(max_length=30)
    def __str__(self):
    	return self.type_name  #改变显示方式

class blog(models.Model,Readnum_extand):  #设置博文的一些属性
    title=models.CharField(max_length=30)
    blog_type=models.ForeignKey(blogtype,on_delete=models.DO_NOTHING) 
    #外键继承  博文的属性
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    Create_time=models.DateTimeField(auto_now_add=True)
    last_update_time=models.DateTimeField(auto_now=True)

    
        
    def __str__(self):
        return '<blog：%s>' % self.title
    class Meta:
        ordering=['-Create_time']   #按照创建的时间排序
'''
class Readnum(models.Model):
    read_num=models.IntegerField(default=0)  #阅读计数
    the_blog=models.OneToOneField(blog,on_delete=models.DO_NOTHING)#通过外键关联到特定的blog,是一对一的关系
'''