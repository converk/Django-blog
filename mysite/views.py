from django.shortcuts import render,redirect
from blog.models import blog
from django.contrib.contenttypes.models import ContentType
from read_count.utils import get_seven_days_read
from django.contrib.auth import authenticate, login
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User

def home(request):
	content_type=ContentType.objects.get_for_model(blog)  #获取模型
	dates,result_list=get_seven_days_read(content_type)

	context={}
	context['dates']=dates
	context['result_list']=result_list  #传递给前端页面
	return render(request,'home.html',context)


def userlogin(request):
	'''
    username = request.POST.get('username','')#接收前端传来的数据(是一个字典),如果get不到,返回空字符
    password = request.POST.get('password','')
    referer = request.META.get('HTTP_REFERER','/')  #得到登陆之前的界面信息,得不到返回主页的url
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(referer)  #登录成功返回到登录之前的界面
    else:
        return render(request,'error.html',{'message':'您的信息有误'})  #登录失败返回一个错误界面
	'''
	if request.method == "POST":  #如果请求这个方法的方式是POST
		loginform=LoginForm(request.POST)  #通过request得到用户名和密码
		if loginform.is_valid():
			user=loginform.cleaned_data['user']  #这里的user已经在models里面验证过了
			login(request, user)
			return redirect(request.GET.get('from','/'))  #登录成功返回到登录之前的界面get不到则返回到主页
	else:  #如果请求这个方法的方式不是POSt,专加载这个页面,
		loginform=LoginForm()
	context={}
	context['loginform']=loginform
	return render(request,'userlogin.html',context)


def register_user(request):  #注册用户
	if request.method == "POST":
		regform=RegForm(request.POST)
		if regform.is_valid():
			username=regform.cleaned_data['username']
			email=regform.cleaned_data['email']
			password=regform.cleaned_data['password']
			#创建用户
			user=User.objects.create(username,email,password)
			user.save()

			#登录
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect(request.GET.get('from','/'))  #登录成功返回到登录之前的界面get不到则返回到主页
	else:
		regform=RegForm()
	context={}
	context['regform']=regform
	return render(request,'register.html',context)