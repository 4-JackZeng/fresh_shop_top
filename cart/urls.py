from django.conf.urls import url

from cart import views

urlpatterns=[
    #添加到购物车
    url(r'add_cart/',views.add_cart,name='add_cart'),
    #购物车页面
    url(r'^cart/',views.cart,name='cart'),
    #购物车价格
    url(r'^f_price/', views.f_price, name='f_price'),
    #购物车数量
    url(r'^f_nums/',views.f_nums,name='f_nums'),
    url(r'^check/', views.check, name='check'),
]