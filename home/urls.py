from django.conf.urls import url

from home import views
urlpatterns =[
    #主界面
    url(r'^index/',views.index,name='index'),
    # 更多商品列表
    url(r'^list/(\d)(\d)(\d+)$',views.list,name='list'),

]