from django import forms

SEX_CHOICES = [('男','male'),('女','female')]
LAN_CHOICES = [('javascript','javascript'),('Python','Python'),('C++','C++'),('C','C'),('Node','Node')]
AREA_CHOICES = (
  ('前端',(('React','React'),('React Native','React Native'),('Vue','Vue'),('Webpack','Webpack'),('Node','Node'),('Flutter','Flutter'))),
  ('后端',(('Node','Node'),('Express','Express'),('Koa','Koa'),('Django','Django'))),
)

class Register(forms.Form):
  user_name = forms.CharField(label='注册用户名', max_length=10, required=True)
  password = forms.CharField(label='密码', max_length=30, required=True)
  password_again = forms.CharField(label='密码确认', max_length=30, required=True)
  avatar = forms.ImageField(label='头像上传', required=False)
  sex = forms.ChoiceField(label='性别', choices=SEX_CHOICES, required=False)
  #program_lan = forms.MultipleChoiceField(label='使用编程语言', choices=LAN_CHOICES, required=False)
  #study_area = forms.MultipleChoiceField(label='研究领域', choices=AREA_CHOICES, required=False)