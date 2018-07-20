from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
	#评论不一定是评论博客,也有可能是评论其他的model  ,所以要用contenttype关联起来
	#评论的内容,时间,对象,评论者
	content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	text=models.TextField()  #评论的内容,不限长度
	comment_time=models.DateTimeField(auto_now_add=True)  #自动添加评论的时间
	user=models.ForeignKey(User,on_delete=models.DO_NOTHING)  #删除评论的时候,不影响用户的数据
	


