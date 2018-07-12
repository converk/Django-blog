from django.shortcuts import render_to_response
from blog.models import blog
from django.contrib.contenttypes.models import ContentType
from read_count.utils import get_seven_days_read

def home(request):
	content_type=ContentType.objects.get_for_model(blog)  #获取模型
	dates,result_list=get_seven_days_read(content_type)

	context={}
	context['dates']=dates
	context['result_list']=result_list  #传递给前端页面
	return render_to_response('home.html',context)