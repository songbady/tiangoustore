from django.db import models
from user.models import user
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from user.models import user,reciver
from good.models import good
from order.models import order
import math
from django.core.paginator import Paginator
import re
from django.urls import reverse


# Create your views here.
def Login(request):
    if request.method=='GET':
        
        return render(request,'login.html')
    else:
        #获取输入的用户名和密码
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        
        #判断数据库中有无该用户    
        isuser=user.objects.filter(username=name).exists()
        if (isuser):
            #判断用户是否被禁用
            nowuser=user.objects.get(username=name)
            if (nowuser.ban==1):
                    return render(request,'login.html',{'error_msg':'该用户已被禁用！'})
            #若该用户存在，获取真的密码
            rel_pwd=user.objects.filter(username=name).get(username=name).password
            cur_user=user.objects.filter(username=name).get(username=name)
            if rel_pwd==pwd:
                    #密码正确，则将用户id存入session，同时记录登录状态
                    #设置退出浏览器清除session
                    request.session.set_expiry(0)
                    request.session['u_id']=str(cur_user.u_id)
                    
                    request.session['islogin']='1'
                    print(request.session)
                    
                    rep=redirect('/')
                    
                   
                    return rep
            else:
                #密码错误，返回提示信息
                return render(request,'login.html',{'error_msg':'密码错误！'})
        else:
            #数据库中没有该用户，返回提示信息
            return render(request,'login.html',{'error_msg':'该用户还未注册！'})
#注册功能
def Register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        #获取输入的用户名和密码
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        #判断数据库中有无该用户名
        isuser=user.objects.filter(username=name).exists()
        if (isuser):
            #若已有该用户名，提醒已注册
            return render(request,'register.html',{'error_msg':'该用户已经注册！'})
        else:
            #若没有，在数据库添加该用户，并跳转至登录界面
            u=user.objects.create(username=name,password=pwd,email=request.POST.get('email'),phone='')
            return redirect('/user/login/')
#退出登录
def Logout(request):
    #清空session内的内容，并返回主页
    request.session.clear()
    request.session['u_id']=''
   
    return redirect('/')
def perInf(request):
    
    if request.method=='GET':
        #判断是否已经登录
        if request.session.get('islogin')=='1':
            #从session获取用户id
            curr_u_id=int(request.session.get('u_id'))
            #查询用户
            curr_user=user.objects.get(u_id=curr_u_id)
            return render(request,'user_center_info.html',{'user':curr_user,'num':1})
        else:
            #跳转至登录界面
            return redirect('/user/login/')
    else:
        #请求方式为post，代表需要更改信息
        a=request.POST
        #获取输入信息
        new_phone=a.get('phone')
        new_email=a.get('email')
        #更新数据库信息
        user.objects.filter(u_id=request.session.get('u_id')).update(phone=new_phone,email=new_email)
        curr_user=user.objects.get(u_id=request.session.get('u_id'))
        return render(request,'user_center_info.html',{"user":curr_user,'num':1})
def showorders(reqeust,num):
    num=int(num)
    #查询所有订单
    orderlist=order.objects.filter(u_id=int(reqeust.session.get('u_id')))
    #分页显示
    pager=Paginator(orderlist,1)
    #获取当前页面订单
    page_orderlist=pager.page(num)
    #计算开始页码
    begin=(num-int(math.ceil(10.0/2)))
    if begin<1:
        begin=1
    #计算结束页码
    end=begin+9
    if end>pager.num_pages:
        end=pager.num_pages
    if end<=10:
        begin=1
    else:
        begin=end-9
    pagelist=range(begin,end+1)  
    return render(reqeust,'user_center_order.html',{'orderlist':page_orderlist,'pagelist':pagelist})

def placeorder(request,oid):
    
    oid=int(oid)
    #获取当前订单
    curr_order=order.objects.get(o_id=oid)
     #获取商品
    curr_good=good.objects.get(g_id=curr_order.g_id)
    total_price=curr_order.price
    count=curr_order.o_number
    
   
    #获取地址
    uid=request.session.get('u_id')
    hasaddress=reciver.objects.filter(u_id=uid).exists()
    curr_reciver=reciver.objects.filter(u_id=uid).order_by('createtime').last()

   
    #设置运费，默认10元，满50免运费
    if (total_price>=50):
        transit_price=0
    else:
        transit_price=10
    total_pay=total_price+transit_price
    return render(request,'place_order.html',{'good':curr_good,'total_price':total_price,'transit_price':transit_price,'total_count':count,'total_pay':total_pay,'num':1,'curr_order':curr_order,'hasaddress':hasaddress,'reciver':curr_reciver})

def addresschange(request):


    if request.method=='GET':
            #从session获取用户id
            uid=int(request.session.get('u_id'))
            hasaddress=reciver.objects.filter(u_id=uid).exists()
            curr_reciver=reciver.objects.filter(u_id=uid).order_by('createtime').last()
           
            return render(request,'user_center_site.html',{'reciver':curr_reciver,'hasaddress':hasaddress,'num':1})
    else:
        uid=int(request.session.get('u_id'))
        hasaddress=reciver.objects.filter(u_id=uid).exists()
        curr_reciver=reciver.objects.filter(u_id=uid).order_by('createtime').last()
        #user=request.user #用户名
        uid=request.session.get('u_id')
        name=request.POST.get('r_name') #收件人
        province = request.POST.get('r_province') #地址
        city = request.POST.get('r_city')
        district = request.POST.get('r_district')
        address=request.POST.get('r_address')
        zipcode = request.POST.get('r_zipcode') #邮编
        phone = request.POST.get('r_phone') #手机号码

        # 2.校验数据
        if not all([name,province,city,district,address,zipcode,phone]):
            return render(request, 'user_center_site.html', {'errmsg': '输入不完整','reciver':curr_reciver,'hasaddress':hasaddress,'num':1})

        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确','reciver':curr_reciver,'hasaddress':hasaddress,'num':1})

        reciver.objects.create(u_id=uid,r_name=name,r_province=province,r_city=city,r_district=district,r_address=address,
                                r_zipcode=zipcode,r_phone=phone)#is_default=is_default)
        #Address.objects.filter(u_id=request.session.get('u_id')).update(r_name=r_name,r_province=r_province,r_city=r_city,
        #                                       r_district=r_district,r_alias=r_alias,r_zipcode=r_zipcode,r_phone=r_phone)
                                                                       
        return HttpResponseRedirect(reverse("user:addsite_show"))  # get请求

    