from django.conf.urls import url

from orders import views

urlpatterns=[

    url(r'^order/',views.order,name='order')
]