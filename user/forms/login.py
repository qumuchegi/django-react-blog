from django import forms

class Login(forms.Form):
  user_name = forms.CharField(label='注册用户名', max_length=10, required=True)
  password = forms.CharField(label='密码', max_length=30, required=True)