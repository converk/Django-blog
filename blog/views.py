from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator   #导入分页器
from django.db.models import Count #导入计算每个类型博客数量的所需的类
from django.contrib.contenttypes.models import ContentType
from read_count.models import Readnum,Readnum_extand,Readnum_detail
from django.utils import timezone
from read_count import utils
from .models import blog,blogtype
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.
#这是显示在主页上的
def get_blog_common_data(request,blogs_all_list):   #代码中重复的部分
	context={}
	paginator=Paginator(blogs_all_list,6)   #把博客按照10个一页分页
	page_num=request.GET.get('page',1)  #获得url页面的page参数值(get请求),也就是当前页数
	page_of_blogs=paginator.get_page(page_num)   #获得这个页数内的信息  不合法就返回默认的页数
	current_page_number=page_of_blogs.number  #获得当前页码
	#获取一个列表,让前端只显示少前后三四页  并对首页和尾页进行处理
	page_range=[i for i in range(current_page_number-3,current_page_number+4) if i in paginator.page_range]
	#在间距过大的页数之间加入省略号
	if page_range[0]-1>=2:
		page_range.insert(0,'...')
	if paginator.num_pages-page_range[-1]>2:
		page_range.append('...')
	#加上首页和尾页
	if page_range[0]!=1:
		page_range.insert(0,1)
	if  page_range[-1]!=paginator.num_pages:  #num_pages获取分页后共有多少页
		page_range.append(paginator.num_pages)

	#获取相应博客类型的数量
	'''blog_types_list=[]
	blog_types=blogtype.objects.all()
	for blog_type in blog_types:
		blog_type.blog_count=blog.objects.filter(blog_type=blog_type).count()  #获取相应博客类型的数量
		blog_types_list.append(blog_type)  #blog_type里面有一个blog_count的属性
	'''
	blogtype.objects.annotate(blog_count=Count('blog'))  #blog_count可以看做说明每个类型的数量的属性
	#获取相应时间的博客数量
	blog_dates=blog.objects.dates('Create_time','month',order='DESC')
	blog_dates_dict={}
	for blog_date in blog_dates:
		blog_count=blog.objects.filter(Create_time__year=blog_date.year,Create_time__month=blog_date.month).count()
		blog_dates_dict[blog_date]=blog_count   #由于不是外键,所以不能像类型那样直接使用属性



	context['page_range']=page_range
	context['page_of_blogs']=page_of_blogs  #为了使用模板blog_list.thml
	context['blog_types']=blogtype.objects.annotate(blog_count=Count('blog'))
	context['blog_dates']=blog_dates_dict
	return context

def blog_list(request):  #创建博客的列表
	blogs_all_list=blog.objects.all()   #获得所有博客
	context=get_blog_common_data(request,blogs_all_list)
	return render(request,'blog_list.html',context)



def blogs_all_of_the_type(request,blog_type_id):
	blog_type=get_object_or_404(blogtype,pk=blog_type_id)	#按照type的顺序id得到对应的type名称
	blogs_all_list=blog.objects.filter(blog_type=blog_type)   #获得所有符合要求博客
	context=get_blog_common_data(request,blogs_all_list)
	context['blogs_all_of_the_type']=blog.objects.filter(blog_type=blog_type)	#通过blog_type来过滤相应的博客
	context['blog_type']=blog_type   #保存blog_type的名字，在html中会用到
	return render(request,'blogs_all_of_the_type.html',context)



def blogs_with_date(request,year,month):  #代码与之前的大多是重复的
	blogs_all_list=blog.objects.filter(Create_time__year=year,Create_time__month=month)   #获得所有符合要求博客
	context=get_blog_common_data(request,blogs_all_list)
	context['blogs_all_of_the_date']=blog.objects.filter(Create_time__year=year,Create_time__month=month)
	context['date']='%s-%s' %(year,month)
	return render(request,'blogs_all_of_the_date.html',context)




def blog_detail(request,blog_id):  #显示博客的具体信息
    the_blog=get_object_or_404(blog,pk=blog_id)  #获得一个blog的所有属性  得不到就返回404
    if not request.COOKIES.get('blog_%s_readed' % blog_id): #当cookie不存在的时候才会进行总阅读数
        cn=ContentType.objects.get_for_model(blog)
        #对于总阅读数
        #如果get不到,就创建这个记录
        readnum,created=Readnum.objects.get_or_create(content_type=cn,object_id=blog_id)
        readnum.read_num+=1
        readnum.save()

        #对于当天的阅读数
        date=timezone.now().date()  #获取一天的日期
        readnum_detail,created=Readnum.objects.get_or_create(content_type=cn,object_id=blog_id)
        readnum_detail.read_num+=1
        readnum_detail.save()

    blog_content_type=ContentType.objects.get_for_model(the_blog)
    comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog_id)

    context={}
    context['blog']=the_blog
    #获得该篇博客的上一篇博客,用过滤器筛选,然后选择最后一个 __gt是大于这个创建时间
    context['previous_blog']=blog.objects.filter(Create_time__gt=the_blog.Create_time).last()
    #获得该篇博客的下一篇博客,用过滤器筛选,然后选择第一个 __lt是小于这个创建时间
    context['next_blog']=blog.objects.filter(Create_time__lt=the_blog.Create_time).first()
    context['comments']=comments

    #data是初始化
    data={}
    data['content_type']=blog_content_type.model  #获模型名
    data['object_id']=blog_id  #获取id名
    context['commentform']=CommentForm(initial=data)  #实例化comment的文本框  #初始化,给隐藏的content_type与object_id一个默认值
    response=render(request,'blog_detail.html',context)
    response.set_cookie('blog_%s_readed' % blog_id,'true')  
    #为已经阅读过的blog设置cookie,没有设置失效时间就是当浏览器关闭的时候才会失效
    return response
