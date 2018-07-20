from django import forms   #使用forms类来进行表单提交,就不必使用后端来接收前端返回的表单信息

class LoginForm(forms.Form):
	username = forms.CharField(label='用户名')
	password = forms.CharField(label='密码',widget=forms.PasswordInput)  #widget是设置密码为暗文