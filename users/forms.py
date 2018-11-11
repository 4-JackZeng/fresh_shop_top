from django import forms
from users.models import User




class UserRegisterForm(forms.Form):
    """用户注册验证表单"""
    user_name=forms.CharField(required=True,max_length=20,min_length=5,error_messages={'required':'账号必填','max_length':'用户名不超过20个字符','min_length':'用户名不少于5个字符'})
    pwd=forms.CharField(max_length=20,min_length=8,required=True,error_messages={'required':'再次确认密码','max_length':'密码不超过20个字符','min_length':'密码不少于5个字符'})
    cpwd=forms.CharField(max_length=20,min_length=8,required=True,error_messages={'required':'再次确认密码','max_length':'密码不超过20个字符','min_length':'密码不少于5个字符'})
    email=forms.CharField(required=True,error_messages={'required':'邮箱必填'})
    allow=forms.BooleanField(required=True,error_messages={'required':'勾选协议'})

    def clean(self):
        username=self.cleaned_data.get('user_name')
        pwd=self.cleaned_data.get('pwd')
        cpwd=self.cleaned_data.get('cpwd')
        # 校验用户名是否注册
        user = User.objects.filter(username=username)
        if user:
            raise forms.ValidationError({'user_name': '用户名存在'})
        if pwd!=cpwd:
            raise forms.ValidationError({'cpwd':'二次密码不一致'})
        return self.cleaned_data


class UserLoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(required=True, max_length=20, min_length=5,
                                error_messages={'required': '账号必填', 'max_length': '用户名不超过20个字符',
                                                'min_length': '用户名不少于5个字符'})
    pwd = forms.CharField(max_length=20, min_length=8, required=True,
                          error_messages={'required': '再次确认密码', 'max_length': '密码不超过20个字符', 'min_length': '密码不少于5个字符'})

    def clean_username(self):
        # 校验用户名是否已经注册过
        username=self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            # 如果已经注册过
            raise forms.ValidationError({'username': '用户没注册'})
        return username
