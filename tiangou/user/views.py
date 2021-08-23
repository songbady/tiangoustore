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
        
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        
            
        isuser=user.objects.filter(username=name).exists()
        if (isuser):
        
            rel_pwd=user.objects.filter(username=name).get(username=name).password
            cur_user=user.objects.filter(username=name).get(username=name)
            if rel_pwd==pwd:
                    
                    request.session['username']=cur_user.username
                    request.session['phone']=cur_user.phone
                    request.session['email']=cur_user.email
                    
                    rep=redirect('/user/perInf/')
                    
                   
                    return rep
            else:
                return render(request,'login.html',{'error_msg':'密码错误！'})
        else:
            return render(request,'login.html',{'error_msg':'该用户还未注册！'})
def Register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        isuser=user.objects.filter(username=name).exists()
        if (isuser):
            return render(request,'register.html',{'error_msg':'该用户已经注册！'})
        else:
            u=user.objects.create(username=name,password=pwd,email=request.POST.get('email'),phone='11111111')
            return HttpResponse('注册成功')

def perInf(request):
    if request.method=='GET':
        return render(request,'user_center_info.html',{'username':request.session.get('username'),'phone':request.session.get('phone'),'email':request.session.get('email')})
    else:
       
        a=request.POST
        new_phone=a.get('phone')
        new_emai=a.get('email')
        print(new_phone)
        print(new_emai)
        user.objects.filter(username=request.session.get('username')).update(phone=new_phone,email=new_emai)
        request.session['phone']=new_phone
        request.session['email']=new_emai
        return render(request,'user_center_info.html',{'username':request.session.get('username'),'phone':request.session.get('phone'),'email':request.session.get('email')})