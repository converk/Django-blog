from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

def submit_comment(request):
	referer = request.META.get('HTTP_REFERER','/')   #重定向到这个界面
	commentform = CommentForm(request.POST)  #提交评论一定是post请求
	if not request.user.is_authenticated:   #由于form里面没有user参数,所以user的验证只好在views里面进行
		return render(request,'error.html',{'message':'用户未登录'})

	if commentform.is_valid():  #如果这个form表单是可以用的,就新生成一个评论
		comment = Comment()
		comment.user=request.user
		comment.text=commentform.cleaned_data['text']
		comment.content_object=commentform.cleaned_data['content_object']
		comment.save()
		return redirect(referer)
	else:
		return render(request,'error.html',{'message':commentform.errors})  #将错误传到前端页面
