from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from good.models import*
from order.models import*
from django.core.paginator import Paginator
import math
from user.models import reciver
# Create your views here.
def placeorder(request,gid):
    count=int(request.GET.get('count'))
    gid=int(gid)
     #获取商品
    curr_good=good.objects.get(g_id=gid)
    total_price=count*curr_good.g_price #商品总价
    #创建一个未付款的订单
    order.objects.create(u_id=int(request.session.get('u_id')),g_id=gid,o_number=count,pay_status=0,price=total_price)
    #获取当前订单
    curr_order=order.objects.filter(u_id=int(request.session.get('u_id'))).order_by('time').last()
   
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
    return render(request,'place_order.html',{'good':curr_good,'total_price':total_price,'transit_price':transit_price,'total_count':count,'total_pay':total_pay,'num':1,'curr_order':curr_order,'reciver':curr_reciver,'hasaddress':hasaddress})
def payorder(request,oid):
    oid=int(oid)
    #获取该订单
    curr_order=order.objects.get(o_id=oid)
    #检查有无默认地址
   
    if not (reciver.objects.filter(u_id=int(request.session.get('u_id')))).exists():
        msg='您没有默认地址'
        msg1='编辑地址'
        url='/user/addsite_show/'
        return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
    
    #检查订单是否已经支付
    if (curr_order.pay_status==1):
        msg='该订单已经支付过了'
        msg1='返回首页'
        url='/'
        return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
    else:
  
        #获取商品
        curr_good=good.objects.get(g_id=curr_order.g_id)
        print(curr_good.g_id)
        print(curr_order.g_id)
        #判断商品是否下架
        if (curr_good.g_status):
            #判断库存是否充足
            if(curr_order.o_number>curr_good.g_total):
                msg='库存不足'
                msg1='返回首页'
                url='/'
                return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
            else:
                #减少商品库存
                good.objects.filter(g_id=curr_order.g_id).update(g_total=curr_good.g_total-curr_order.o_number)
                
                #订单状态设为已支付
                order.objects.filter(o_id=oid).update(pay_status=1)
                msg='支付成功'
                msg1='返回首页'
                url='/'
                return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
        else:
            msg='商品已下架'
            msg1='返回首页'
            url='/'
            return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
#查看物流
def showlogistics(request):
    return HttpResponse('该订单正在配中中！')