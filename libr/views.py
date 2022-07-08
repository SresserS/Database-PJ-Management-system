from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from requests import request
from startlib import forms,models
from startlib.models import nor_admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import requests
import re
import json

##普通管理员登录
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['用户名']
        password = request.POST['密码']
        user = authenticate(request, username=username, password=password)
        if user is None:
            str='登录失败'
            return render(request, 'login.html', {'失败': str})
        else:
            login(request, user)
            return redirect('mainpage')
    else:
        return render(request, 'login.html')

##超级管理员登录
def superlogin(request):
    if request.method == 'POST':
        username = request.POST['用户名']
        password = request.POST['密码']
        if username=='SresserS':
            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'失败': '账号密码错误'})
            else:
                login(request, user)
                return redirect('mainpage')
        else:
            return render(request, 'login.html', {'失败': '不是超级管理员'})
    else:
        return render(request, 'login.html')


##注册普通管理员
@login_required(login_url='superlogin')
def register(request):
    if request.method == 'POST':
        register_form = forms.registerform(request.POST)
        if register_form.is_valid():
            register_form.save()
            username=register_form.cleaned_data['username']
            password=register_form.cleaned_data['password1']
            usera=authenticate(username=username, password=password)
            '''register_form.save()
            user=authenticate(username=register_form.cleaned_data['username'], 
                    password=register_form.cleaned_data['password'])
            models.nor_admin.objects.create(user,name=register_form.cleaned_data['name'],
                        ID=register_form.cleaned_data['ID'],
                        gender=register_form.cleaned_data['gender'],
                        age=register_form.cleaned_data['age'],
                        phone=register_form.cleaned_data['phone'])
            login(request,user)
            return redirect('mainpage')##############'''
            #username = register_form.cleaned_data['username']
            #password = register_form.cleaned_data['password1']
            name=register_form.cleaned_data['personname']
            ID=register_form.cleaned_data['pID']
            gender=register_form.cleaned_data['gender']
            age=register_form.cleaned_data['age']
            phone=register_form.cleaned_data['phone']
            models.nor_admin.objects.create(user=usera,name=name,ID=ID,gender=gender,age=age,phone=phone)
            login(request,usera)
            return redirect('mainpage')
        else:
            return HttpResponse('错误')
    else: 
        register_form = forms.registerform()
    return render(request,'register.html')

@login_required(login_url='superlogin')
def select_admin(request):
    if request.method == 'GET':
        keyword=request.GET.get('keyword')
        if (not keyword):
            list = models.nor_admin.objects.all()
            return render(request,'select_admin.html',{'list':list})
        else:
            list = models.nor_admin.objects.filter( Q(name__contains=keyword) 
                    | Q(ID__contains=keyword) | Q(gender__contains=keyword)
                    | Q(age__contains=keyword) | Q(phone__contains=keyword) )
            return render(request,'select_admin.html',{'list':list})
    else:
        return render(request,'select_admin.html')

@login_required(login_url='login')
def update_admin(request):
    user=request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        ID = request.POST.get('ID')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        if user.username==username and authenticate(username,password):
            models.nor_admin.objects.filter(ID=ID).update(name=name,ID=ID,
                        gender=gender,age=age,phone=phone)
            return redirect('mainpage')
        else:
            return render(request,'update_admin.html')
    elif request.method == 'GET':
        admid = request.GET.get('admid')
        adm = models.nor_admin.objects.filter(ID=admid).first()
        return render(request,'update_admin.html',{'adm':adm})
    else:
        return render(request,'update_admin.html')

def logoutuser(request):
    logout(request)
    return redirect('mainpage')

def dangdang(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None

def ans(html):
    pattern = re.compile(
        '<li.*?list_num.*?(\d+)\.</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span class="price_n">(.*?)</span>.*?</li>', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'recommend': item[3],
            'author': item[4],
            'times': item[5],
            'price': item[6]
        }

def mainpage(request):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(1)
    html = dangdang(url)
    items = ans(html)
    return render(request,'mainpage.html',{'items':items})


