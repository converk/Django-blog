from django import forms   #使用forms类来进行表单提交,就不必使用后端来接收前端返回的表单信息
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"用户名"}))
	password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"密码"}))  
	#widget是设置密码为暗文
	#form-control是bootstrap设置表单控制样式要用到的
	#placeholder是输入框默认值
	#在class里面可以添加你想为这个标签添加的class

	def clean(self):  #将验证身份放在model里面
		username=self.cleaned_data['username']    #接受从前端传来的数据
		password=self.cleaned_data['password']

		user = authenticate(username=username, password=password)  ##这里的判断用户不需要request
		if user is None:  #当用户名和密码不正确
			raise forms.ValidationError('用户名或者密码不正确')
		else:
			self.cleaned_data['user']=user
		return self.cleaned_data  #当验证通过的时候,返回清理后的数据


class RegForm(forms.Form):  #注册用户

	username = forms.CharField(label='用户名',
								max_length=30,  #用户名最长字数
								min_length=3,  #最短字数
								widget=forms.TextInput(attrs={'class':'form-control','placeholder':"请输入用户名"}))
	password = forms.CharField(label='密码',
								min_length=6,
								widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"请输入密码"}))  
	email = forms.EmailField(label='电子邮箱',
							widget=forms.EmailInput(attrs={'class':'form-control','placeholder':"请输入电子邮箱"}))
	password_again = forms.CharField(label='密码',
								min_length=6,
								widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"请再输入一次密码"}))
	
	def clean_username(self):  #判断用户名是否重复
		username=self.cleaned_data['username']
		if User.objects.filter(username=username).exit():
			raise forms.ValidationError('用户名已经存在')
		return username

	def clean_email(self):  #判断邮箱是否已经存在
		email=self.cleaned_data['email']
		if User.objects.filter(email=username).exit():
			raise forms.ValidationError('邮箱已经存在')
		return email

	def clean_password(self):
		password=self.cleaned_data['password']
		password_again=self.cleaned_data['password_again']
		if password_again != password:
			raise forms.ValidationError('两次密码不一致!')
		return password