from django import forms  
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist  #对象获取不存在的时候报的错误
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput())
	object_id = forms.IntegerField(widget=forms.HiddenInput())
	text = forms.CharField(widget=CKEditorWidget())  #设置为可以多行输入的文本域

	#验证是否通过
	def clean(self):
		content_type = self.cleaned_data['content_type']
		object_id = self.cleaned_data['object_id']
		try:
			model_class=ContentType.objects.get(model=content_type).model_class()
			model_obj=model_class.objects.get(pk=object_id)
			self.cleaned_data['content_object']=model_obj   #在view里面实例化的时候需要用到content_object
		except ObjectDoesNotExist:
			raise forms.ValidationError('对象不存在')

		return self.cleaned_data
