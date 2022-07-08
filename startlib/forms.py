from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class registerform(UserCreationForm):
    #username = forms.CharField(label = '用户名', max_length=20)
    #password1 = forms.CharField(label="密码", max_length=20)
    #password2 = forms.CharField(label="密码", max_length=20)
    personname = forms.CharField(required=True,max_length=40)
    pID = forms.CharField(required=True,max_length=40)
    gender = forms.CharField(required=True,max_length=10)
    age = forms.CharField(required=True,max_length=10)
    phone = forms.CharField(required=True,max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1','password2','personname', 'pID', 'gender','age','phone')
        
