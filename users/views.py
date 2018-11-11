from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm,UserRegisterForm
from users.models import User



def register(request):
    if request.method=='GET':

        return render(request,'register.html')
    if request.method=='POST':
        #校验页面中传递的参数，是否填写完整
        # username=request.POST.get('username')
        # 将request.POST的内容交给Form校验，得到一个form
        # 表单验证，是否有效
        # 验证通过后,使用自定义Users.objects.create
        form=UserRegisterForm(request.POST)
        #is_valid()判断表单是否有效
        if form.is_valid():
            User.objects.create(username=form.cleaned_data['user_name'],
                                password=make_password(form.cleaned_data['pwd']),
                                email=form.cleaned_data['email']  )
            #注册成功



            #实现跳转
            return HttpResponseRedirect(reverse('users:login'))

            # return render(request,'register.html')
            # else:
            #     return render(request,'register.html')
        # 如果校验不通过，页面跳转到注册页面，并且返回form，from里包含from.errors信息，可以在输入框上面显示错误信息
        else:
            return render(request,'register.html',{'form':form})

def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    if request.method =='POST':
        #1.表单验证
        form=UserLoginForm(request.POST)
        if form.is_valid():
            user=User.objects.filter(username=form.cleaned_data['username']).first()

            if not check_password(form.cleaned_data['pwd'],user.password):

                return HttpResponseRedirect(reverse('users:login'))

            request.session['user_id']=user.id
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return render(request, 'login.html', {'form': form})


def logout(request):
    if request.method=='GET':
        del request.session['user_id']
        return HttpResponseRedirect(reverse('users:login'))
