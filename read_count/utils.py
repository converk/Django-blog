from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Readnum,Readnum_detail
from django.db.models import Sum   #导入聚合的方式
import datetime

def get_seven_days_read(content_type):  #获取七天的阅读数,不一定是什么模型,所以为了通用引入一个content_type参数
	today=timezone.now().date()   #获得今天的日期
	result_list=[]
	dates=[]
	for i in range(7,-1,-1):  #倒叙从7到1
		day_date=today-datetime.timedelta(days=i)  #这个是为了获得与今天相差i天的日期
		dates.append(day_date.strftime('%m/%d'))  #把datetime类型的day_date转化为str类型
		today_read_blogs=Readnum_detail.objects.filter(content_type=content_type,date=day_date)  #获得这一天所读的所有博客
		result=today_read_blogs.aggregate(read_num_all_the_day=Sum('read_num'))
		#这里是聚合,aggregate是聚合函数,Sum是聚合的方法,'read_num'是对哪一项进行聚合,today_read_blog是今天阅读过的博客集合
		#返回值是一个字典,字典的key是read_num_all_the_day,字典的value就是聚合的结果
		result_list.append(result['read_num_all_the_day'] or 0)  
		#将七天的阅读结果都放到list中,如果哪一天的结果为None,通过or 0,让None变成0
	return dates,result_list