from django.db import models
import django.utils.timezone as tz
from django.contrib.auth.models import User
from sqlalchemy import true


class book(models.Model):
    bookid = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=20)
    name = models.CharField(max_length=40)
    publisher = models.CharField(max_length=40)
    author = models.CharField(max_length=40)   
    price = models.DecimalField(max_digits=6, decimal_places=2)
    storenum = models.IntegerField(default=0)######################删除##########################

class nor_admin(models.Model):
    #username = models.CharField(max_length=40)
    #password = models.CharField(max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)##########name重复
    ID = models.CharField(max_length=40)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    class Meta:
        verbose_name = 'nor_admin'

class incomebooks(models.Model):
    incomeid = models.AutoField(primary_key=True)
    bookid = models.ForeignKey(to='book',on_delete=models.DO_NOTHING)
    inprice = models.DecimalField(max_digits=6, decimal_places=2)
    innum = models.IntegerField(default=0)
    state = models.CharField(max_length=20) ##如果不在book里面？
    storeid = models.ForeignKey(to='store',on_delete=models.DO_NOTHING,default=1)
    #wstoreid = models.ForeignKey(to='warestorage',on_delete=models.DO_NOTHING)


######################################################删除#####################################################
class finance(models.Model):
    finaceid = models.AutoField(primary_key=True)
    bookid = models.ForeignKey(to='book',on_delete=models.DO_NOTHING)
    fnum = models.IntegerField(default=0)
    ftime = models.DateTimeField(default=tz.now)
    fstate = models.CharField(max_length=20)#'收入/支出'  


##收入财务记录(对应购买，sale)
##画ER图时发现不需要连store
class income(models.Model):
    inid = models.AutoField(primary_key=True)
    saleid = models.ForeignKey(to='sale',on_delete=models.DO_NOTHING)
    storeid = models.ForeignKey(to='store',on_delete=models.DO_NOTHING)
    ownerid = models.ForeignKey(to='possession',on_delete=models.DO_NOTHING)
    incometime = models.DateTimeField(default=tz.now)
    insummoney = models.DecimalField(max_digits=13,decimal_places=2)

##支出财务记录(对应进货，incomebooks)
class outcome(models.Model):
    outid = models.AutoField(primary_key=True)
    incomeid = models.ForeignKey(to='incomebooks',on_delete=models.DO_NOTHING)    
    outcometime = models.DateTimeField(default=tz.now)
    ownerid = models.ForeignKey(to='possession',on_delete=models.DO_NOTHING)
    outsummoney = models.DecimalField(max_digits=13,decimal_places=2)
    #storeid = models.ForeignKey(to='store',on_delete=models.DO_NOTHING)    

##销售记录
class sale(models.Model):
    saleid = models.AutoField(primary_key=True)
    bookid = models.ForeignKey(to='book',on_delete=models.DO_NOTHING)
    salenum = models.IntegerField(default=0)
    saletime = models.DateTimeField(default=tz.now)
    storeid = models.ForeignKey(to='store',on_delete=models.DO_NOTHING)
    customer = models.CharField(max_length=40)
    saleprice = models.DecimalField(max_digits=6, decimal_places=2) ###############是否冗余

class possession(models.Model):
    ownerid = models.AutoField(primary_key=True)
    ownername = models.CharField(max_length=40)
    wealth = models.DecimalField(max_digits=13,decimal_places=2,default=0)

##无用
class store(models.Model):
    storeid = models.AutoField(primary_key=True)
    storename = models.CharField(max_length=40)
    storephone = models.CharField(max_length=20)
    storeaddress = models.CharField(max_length=40)
    ownerid = models.ForeignKey(to='possession',on_delete=models.DO_NOTHING)

##仓库，仅仓库信息，实际无用，可以考虑删除
class warehouse(models.Model):
    wareid = models.AutoField(primary_key=True)
    warephone = models.CharField(max_length=20)
    wareaddress = models.CharField(max_length=40)

##存储信息，存储仓库名，书名和数量(总数)
class warestorage(models.Model):
    wstoreid = models.AutoField(primary_key=True)
    bookid = models.ForeignKey(to='book',on_delete=models.DO_NOTHING)
    wareid = models.ForeignKey(to='warehouse',on_delete=models.DO_NOTHING)
    storenum = models.IntegerField(default=0)


