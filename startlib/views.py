from ast import keyword
from os import fstat
from secrets import choice
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from numpy import double
from requests import request
from sqlalchemy import between
from sympy import re
from startlib import forms,models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from decimal import Decimal

# Create your views here.
 
'''def hello(request):
    title = '我是新测试人员'
    add_data = TestQuestion(question_title=title)
    add_data.save()
    return HttpResponse('“{}”,数据添加成功'.format(title))
 
def index(request):
    try:
        response = TestQuestion.objects.all()
        get_data = ' # # '.join([i.question_title for i in response])
    except TestQuestion.DoseNotExist:
        raise Http404('页面不存在!')
    return HttpResponse(get_data)'''
#如何实现显示全部 上面是搜索栏
#成功提示弹窗

################################相当于create,不会增加数量############################
@login_required(login_url='login')
def add_books(request):
    if request.method == 'POST':
        #bookid = request.POST.get('bookid')
        ISBN = request.POST.get('ISBN')
        name = request.POST.get('name')
        publisher = request.POST.get('publisher')
        author = request.POST.get('author')
        price = request.POST.get('price')
        storenum = request.POST.get('storenum')
        models.book.objects.create(ISBN=ISBN,name=name,publisher=publisher,
                        author=author,price=price,storenum=storenum)
        return render(request,'add_books.html')
    else: return render(request,'add_books.html')

@login_required(login_url='login')
def select_books(request):
    if request.method == 'GET':
        bookid = request.GET.get('bookid')
        ISBN = request.GET.get('ISBN')
        name = request.GET.get('name')
        publisher = request.GET.get('publisher')
        author = request.GET.get('author')
        keyword = request.GET.get('关键词')
        storenum = request.GET.get('storenum')
        if (not keyword) and (not bookid) and (not ISBN) and (not name) and (not publisher) and (not author) and (not storenum):
            booklist = models.book.objects.all()
            return render(request,'select_books.html',{'booklist':booklist})
        else: 
            booklist = models.book.objects.filter( Q(bookid__contains=keyword) 
                    | Q(ISBN__contains=keyword) | Q(name__contains=keyword)
                    | Q(publisher__contains=keyword) | Q(author__contains=keyword) )
            booklist = booklist.filter(bookid__contains=bookid, ISBN__contains=ISBN,
                    name__contains=name,publisher__contains=publisher,author__contains=author,storenum=storenum)
            return render(request,'select_books.html',{'booklist':booklist})  
    

@login_required(login_url='login')
def update_books(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        ISBN = request.POST.get('ISBN')
        name = request.POST.get('name')
        publisher = request.POST.get('publisher')
        author = request.POST.get('author')
        price = request.POST.get('price')
        storenum = request.POST.get('storenum')
        models.book.objects.filter(bookid=bookid).update(ISBN=ISBN,name=name,publisher=publisher,
                        author=author,price=price,storenum=storenum)
        return redirect('/startlib/select_books')
    elif request.method == 'GET':
        bookid = request.GET.get('bookid')
        aimbook = models.book.objects.filter(bookid=bookid).first()
        return render(request,'update_books.html',{'aimbook':aimbook})
    return render(request,'update_books.html')

@login_required(login_url='login')
def delete_books(request):
    bookid = request.GET.get('bookid')
    models.book.objects.filter(bookid=bookid).delete()
    return redirect('/startlib/select_books')

##书籍创建后寻找新创键的书籍特定函数？
@login_required(login_url='login')
def inbooks(request):
    if request.method == 'POST':
        #incomeid = request.POST.get('incomeid')
        inprice = request.POST.get('inprice')
        innum = request.POST.get('innum')
        storeid = request.POST.get('storeid')
        ISBN = request.POST.get('ISBN')
        name = request.POST.get('name')
        publisher = request.POST.get('publisher')
        author = request.POST.get('author')
        #price = request.POST.get('price')
        if models.book.objects.filter(ISBN=ISBN,name=name,publisher=publisher).first() is None:
            models.book.objects.create(ISBN=ISBN,name=name,publisher=publisher,
                        author=author,storenum=0,price=0)
        bookid_=models.book.objects.filter(ISBN=ISBN,name=name).first()
        store=models.store.objects.filter(storeid=storeid).first()
        models.incomebooks.objects.create(bookid=bookid_,
                            inprice=inprice,innum=innum,state='未付款',storeid=store)
        return render(request,'inbooks.html')
    elif request.method == 'GET':
        bookid = request.GET.get('bookid')
        aimbook = models.book.objects.filter(bookid=bookid).first()
        return render(request,'inbooks.html',{'aimbook':aimbook})
    else:
        return render(request,'inbooks.html')

##付款 同时增加支出outcome记录,possession减少
'''@login_required(login_url='login')
def inbooks_pay(request):
    if request.method == 'POST':
        incomeid = request.POST.get('incomeid')
        models.incomebooks.objects.filter(incomeid=incomeid).update(state='已付款')
        f=models.incomebooks.objects.filter(incomeid=incomeid).first()
        ownerid = models.store.objects.filter(storeid=f.storeid.storeid).first().ownerid
        owner=models.possession.objects.filter(ownerid=ownerid.ownerid).first()
        outsummoney=f.innum*f.inprice
        income=models.incomebooks.objects.filter(incomeid=incomeid).first()
        models.outcome.objects.create(incomeid=income,ownerid=owner,
                        outsummoney=outsummoney)
        p=models.possession.objects.filter(ownerid=ownerid.ownerid)
        w=p.first().wealth
        p.update(wealth=w-outsummoney)
        return render(request,'inbooks_pay.html')
    elif request.method == 'GET':
        incomeid = request.GET.get('id')
        aim = models.incomebooks.objects.filter(incomeid=incomeid).first()
        return render(request,'inbooks_pay.html',{'aim':aim})
    else:
        return render(request,'inbooks_pay.html')'''         

'''@login_required(login_url='login')
def inbooks_cancel(request):
    if request.method == 'POST':
        incomeid = request.POST.get('incomeid')
        models.incomebooks.objects.filter(incomeid=incomeid).update(state='已退货')
        return render(request,'inbooks_cancel.html')    
    elif request.method == 'GET':
        incomeid = request.GET.get('id')
        aim = models.incomebooks.objects.filter(incomeid=incomeid).first()
        return render(request,'inbooks_cancel.html',{'aim':aim})  
    else:
        return render(request,'inbooks_cancel.html')'''

@login_required(login_url='login')
def inbooks_pay(request):
    incomeid = request.GET.get('id')
    models.incomebooks.objects.filter(incomeid=incomeid).update(state='已付款')
    f=models.incomebooks.objects.filter(incomeid=incomeid).first()
    ownerid = models.store.objects.filter(storeid=f.storeid.storeid).first().ownerid
    owner=models.possession.objects.filter(ownerid=ownerid.ownerid).first()
    outsummoney=f.innum*f.inprice
    income=models.incomebooks.objects.filter(incomeid=incomeid).first()
    models.outcome.objects.create(incomeid=income,ownerid=owner,
                        outsummoney=outsummoney)
    p=models.possession.objects.filter(ownerid=ownerid.ownerid)
    w=p.first().wealth
    p.update(wealth=w-outsummoney)
    return redirect('/startlib/select_inbooks')  

@login_required(login_url='login')
def inbooks_cancel(request):
    incomeid = request.GET.get('id')
    models.incomebooks.objects.filter(incomeid=incomeid).update(state='已退货')
    return redirect('/startlib/select_inbooks')  

##查询进货书籍，提供跳转到付款、移入库存和取消的链接
@login_required(login_url='login')
def select_inbooks(request):
    if request.method == 'GET':
        keyword=request.GET.get('keyword')
        '''incomeid=request.GET.get('incomeid')
        bookid=request.GET.get('bookid')
        inprice=request.GET.get('inprice')
        innum=request.GET.get('innum')
        state=request.GET.get('state')'''
        #if (not incomeid) and (not bookid) and (not inprice) and (not innum) and (not state) and (not keyword):
        if (not keyword):
            list = models.incomebooks.objects.all()
            return render(request,'select_inbooks.html',{'list':list})
        else:
            list = models.incomebooks.objects.filter(Q(incomeid__contains=keyword) | Q(inprice__contains=keyword)
                    | Q(state__contains=keyword) | Q(innum__contains=keyword) )
            return render(request,'select_inbooks.html',{'list':list})
    else:
        return render(request,'select_inbooks.html')

##开发incomebooks选择页面，然后在该页面选择已付款的转移
##库存增加，更新价格
@login_required(login_url='login')
def trans_income_to_books(request):
    if request.method == 'POST':
        incomeid = request.POST.get('incomeid')
        #bookid = request.POST.get('bookid')############################bookid设计有问题
        price = request.POST.get('price')
        ic=models.incomebooks.objects.filter(incomeid=incomeid)
        ic.update(state='已到货')
        icnum=ic.first().innum
        b = models.book.objects.filter(bookid=ic.first().bookid.bookid)
        bnum = b.first().storenum
        b.update(storenum=bnum+icnum,price=price)
        return render(request,'trans_income_to_books.html')
    elif request.method == 'GET':
        id = request.GET.get('id')
        aimbook = models.incomebooks.objects.filter(incomeid=id).first()
        return render(request,'trans_income_to_books.html',{'aimbook':aimbook})
    else:
        return render(request,'trans_income_to_books.html')

'''@login_required(login_url='login')
def select_finance(request):
    if request.method == 'GET':
        finaceid = request.GET.get('financeid')
        bookid = request.GET.get('bookid')
        fnum = request.GET.get('fnum')
        ftime = request.GET.get('ftime')
        fstate = request.GET.get('fstate')
        list = models.finance.objects.filter(Q(finaceid__contains=finaceid) 
                    | Q(bookid__contains=bookid) 
                    | Q(fnum__contains=fnum) | Q(ftime__contains=ftime)
                    | Q(fstate__contains=fstate))
    else:
        return render(request,'select_finance.html')

@login_required(login_url='login')
def add_finance(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        fnum = request.POST.get('fnum')
        fstate = request.POST.get('fstate')
        models.finance.objects.create(bookid=bookid,fnum=fnum,fstate=fstate)
        sn = models.book.objects.filter(bookid=bookid).first()['storenum']
        if fstate == '收入':
            models.book.objects.filter(bookid=bookid).update(
                storenum=sn-fnum)
        elif fstate == '支出':
            models.book.objects.filter(bookid=bookid).update(
                storenum=sn+fnum)
    else:
        return render(request,'add_finance.html')'''


#########################################销售模块########################################
##需要开发一个购买页面（也可以理解为sale维护图形页面）


##两种增加模式，1、直接输入信息，2、在booklist选择，类似update和del
##需要调用add_income自动增加###################待完成
@login_required(login_url='login')
def add_sale(request):
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        salenum = request.POST.get('salenum')
        storeid = request.POST.get('storeid')
        customer = request.POST.get('customer')
        saleprice = request.POST.get('saleprice')
        booknum = models.book.objects.filter(bookid=bookid).first().storenum
        if int(salenum)>booknum:
            return HttpResponse('超出库存上限')
        else: 
            book=models.book.objects.filter(bookid=bookid).first()
            store=models.store.objects.filter(storeid=storeid).first()
            thesale=models.sale.objects.create(bookid=book,salenum=salenum,storeid=store,
                        customer=customer,saleprice=saleprice)
            ownerid=models.store.objects.filter(storeid=storeid).first().ownerid
            owner=models.possession.objects.filter(ownerid=ownerid.ownerid).first()
            insummoney=int(salenum)*Decimal(saleprice)
            models.income.objects.create(saleid=thesale,storeid=store,
                    ownerid=owner,insummoney=insummoney)  
            models.book.objects.filter(bookid=bookid).update(storenum=int(booknum)-int(salenum))          
            p=models.possession.objects.filter(ownerid=owner.ownerid)
            w=p.first().wealth
            p.update(wealth=w+insummoney)
        #return redirect('/startlib/select_books')
            render(request,'add_sale.html')
    elif request.method == 'GET':
        bookid = request.GET.get('bookid')
        aimbook = models.book.objects.filter(bookid=bookid).first()
        return render(request,'add_sale.html',{'aimbook':aimbook})
    return render(request,'add_sale.html')

@login_required(login_url='login')
def select_finance(request):
    if request.method == 'GET':
        starttime = request.GET.get('starttime')
        endtime = request.GET.get('endtime')
        if(not starttime and not endtime):
            incomelist = models.income.objects.all()
            outcomelist = models.outcome.objects.all()
            return render(request,'select_finance.html',{'incomelist':incomelist,'outcomelist':outcomelist})
        incomelist = models.income.objects.filter(incometime__range=(starttime,endtime))
        outcomelist = models.outcome.objects.filter(outcometime__range=(starttime,endtime))
        return render(request,'select_finance.html',{'incomelist':incomelist,'outcomelist':outcomelist})

    else:
        return render(request,'select_finance.html')

##理论上来说不需要
#@login_required(login_url='login')
#def add_income(request):

@login_required(login_url='login')
def add_store(request):
    if request.method == 'POST':
        storename = request.POST.get('name')
        storephone = request.POST.get('phone')
        storeaddress = request.POST.get('address')
        ownerid = request.POST.get('ownerid')
        owner = models.possession.objects.filter(ownerid=ownerid).first()
        models.store.objects.create(storename=storename,storephone=storephone,
                    storeaddress=storeaddress,ownerid=owner)
        render(request,'add_store.html')
    else: return render(request,'add_store.html')

@login_required(login_url='login')
def add_poss(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        wealth = request.POST.get('wealth')
        models.possession.objects.create(ownername=name,wealth=wealth)
        return render(request,'add_poss.html')
    else: 
        return render(request,'add_poss.html')

@login_required(login_url='login')
def select_store(request):
    if request.method == 'GET':
        keyword=request.GET.get('keyword')
        if (not keyword):
            list = models.store.objects.all()
            return render(request,'select_store.html',{'list':list})
        else:
            list = models.store.objects.filter(Q(storeid__contains=keyword) | Q(storename__contains=keyword)
                    | Q(storephone__contains=keyword) | Q(storeaddress__contains=keyword) )
            return render(request,'select_store.html',{'list':list})
    else:
        return render(request,'select_store.html')

@login_required(login_url='login')
def select_owner(request):
    if request.method == 'GET':
        keyword=request.GET.get('keyword')
        if (not keyword):
            list = models.possession.objects.all()
            return render(request,'select_owner.html',{'list':list})
        else:
            list = models.possession.objects.filter(Q(ownerid__contains=keyword) | Q(ownername__contains=keyword)
                    | Q(wealth__contains=keyword))
            return render(request,'select_owner.html',{'list':list})
    else:
        return render(request,'select_owner.html')
