from django.urls import path
from . import views

urlpatterns=[
    path(' ',views.blog_list,name='blog_list'),
    path('<int:blog_id>',views.blog_detail,name='blog_detail'),
    path('type/<int:blog_type_id>',views.blogs_all_of_the_type,name='blogs_all_of_the_type'),
    #定义了一个连接到所有该类型的博客的网址
    path('date/<int:year>/<int:month>',views.blogs_with_date,name='blogs_with_date')
]