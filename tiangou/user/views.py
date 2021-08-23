from django.db import models
from user.models import user
from django.shortcuts import render,redirect
from django.http import HttpResponse
from user.models import user




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
            return render(request,'user_center_info1.html',{'user':curr_user})
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
        return render(request,'user_center_info1.html',{"user":curr_user})
    