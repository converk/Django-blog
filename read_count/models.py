from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

class Readnum(models.Model):
    read_num=models.IntegerField(default=0)  #阅读计数
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class Readnum_extand():  #获取博客的阅读次数,不写在blog里面是为了更好的封装
    def read_num(self):
        try:
	        cn=ContentType.objects.get_for_model(self)
	        nu=self.pk
	        readnum=Readnum.objects.get(content_type=cn,object_id=nu)
	        return readnum.read_num
        except Exception as e:
            return 0
class Readnum_detail(models.Model):  #记录每一天的阅读数
    date=models.DateField(default=timezone.now)  #默认时间为现在时间
    read_num=models.IntegerField(default=0)  #阅读计数
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')