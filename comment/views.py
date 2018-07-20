from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment

def submit_comment(request):
	#获取前端表单提交的四个数据
	user = request.user
	text =request.POST.get('text','')
	content_type=request.POST.get('content_type','')
	object_id=int(request.POST.get('object_id','')) 

	model_class=ContentType.objects.get(model=content_type).model_class()
	model_obj=model_class.objects.get(pk=object_id)

	comment=Comment()  #实例化一个评论
	comment.user=user
	comment.text=text
	comment.content_object =model_obj
	comment.save()

	referer = request.META.get('HTTP_REFERER','/')   #重定向到这个界面
	return redirect(referer)
