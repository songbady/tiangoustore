from collections import Set
from order.models import order

from django.db.models import QuerySet
from django.http import JsonResponse, request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from good.views import detail
# Create your views here.
from django.views import View

from cart.models import cart
from good.models import good
from user.models import reciver, user

class newGood():#一个商品类，里面放着我需要得到的商品信息
    goodName=''#商品名
    goodUnite=''#商品单位
    goodPrice=0#商品单价
    goodUrl=''#商品图片地址
    goodId=0#商品ID
    goodAmount=0#商品数量
    goodTotalPrice=0#商品名
def Cart(request):#跳转到购物车界面
    global userid
    userid = request.session.get('u_id')
    carts = cart.objects.filter(userId=userid)#购物车set，里面放着所有本人的购物车信息
    goodSet = set()#新建一个表，这里有着购物车里的所有商品
    totalCount = 0
    totalPrice = 0
    for aCart in carts:
        totalCount += aCart.goodAmount
        aGood=newGood()
        TheGood=good.objects.filter(g_id=aCart.g_id).first()
        aGood.goodName = TheGood.g_name
        aGood.goodUnite = '件'
        aGood.goodPrice = TheGood.g_price
        aGood.goodUrl = TheGood.g_picture
        aGood.goodId = aCart.g_id
        aGood.goodAmount = aCart.goodAmount
        aGood.goodTotalPrice = aGood.goodPrice * aGood.goodAmount
        totalPrice += aGood.goodTotalPrice
        goodSet.add(aGood)
    return render(request, 'cart.html',{'total_count':totalCount, 'skus':goodSet, 'total_price':totalPrice})

class CartUpdateView(View):
    '''购物车记录更新'''
    def get(self, request,gid):
        # 接收数据
        sku_id = int(gid)
        count = request.GET.get('count')
        print(sku_id)
        print(count)
        # 数据校验
        if not all([sku_id, count]):
            message='数据不完整'
            return detail(request,sku_id,msg=message)

        # 校验添加的商品数量
        try:
            count = int(count)
        except Exception as e:
            # 数目出错
            message='商品数目出错'
            return detail(request,sku_id,msg=message)

        # 校验商品是否存在
        try:
            sku = good.objects.get(g_id=sku_id)
        except cart.DoesNotExist:
            # 商品不存在
            message='商品不存在'
            return detail(request,sku_id,msg=message)

        # 校验商品的库存
        if count > sku.g_total:
            message='商品库存不足'
            return detail(request,sku_id,msg=message)

        #更新购物车表的内容
        
        #加一个判断，如果为空#########################################################################################
        if (cart.objects.filter(userId=int(request.session.get('u_id')),g_id=sku_id).exists()):
            
            newCart = cart.objects.get(userId=int(request.session.get('u_id')),g_id=sku_id)
            total_count=newCart.goodAmount+count
            cart.objects.filter(userId=int(request.session.get('u_id')),g_id=sku_id).update(goodAmount=total_count)
            
        else:
            cart.objects.create(userId=int(request.session.get('u_id')),g_id=sku_id,goodAmount=count)
        # 计算用户购物车中商品的总件数
        total_count = 0
        carts = cart.objects.filter(userId=int(request.session.get('u_id')))
        for aCart in carts:
            total_count += aCart.goodAmount
        # 返回应答
        message='加入购物车成功'
        return detail(request,sku_id,msg=message)


class CartDeleteView(View):
    '''购物车记录删除'''
    def get(self, request,gid):
        '''购物车记录删除'''
        # 接收参数
        sku_id = int(gid)
        # 业务处理:删除购物车记录
        # 计算用户购物车中商品的总件数 {'1':5, '2':3}
        total_count = 0
        userid=int(request.session.get('u_id'))
        result = cart.objects.filter(userId=int(request.session.get('u_id')), g_id=sku_id)
        result.delete()
        for i in range(len(result)):
            result[i].save()
        carts = cart.objects.filter(userId=userid)
        for aCart in carts:
            total_count += aCart.goodAmount

        # 返回应答
        return redirect('/cart/cart/')


def perInf(request):
    # 判断是否已经登录
    if request.session.get('islogin') == '1':
        # 从session获取用户id
        curr_u_id = int(request.session.get('u_id'))
        # 查询用户
        curr_user = user.objects.get(u_id=curr_u_id)
        return redirect('/cart/cart/')
    else:
        # 跳转至登录界面
        return redirect('/user/login/')
def paycart(request):
    data=request.GET
    userid = request.COOKIES.get('userid')
    # 通过获取前端get请求的参数，找到goods_id和对应的数量
    request_data=[]
    for key,value in data.items():
        if key.startswith('goods'):
            goods_id = key.split('_')[1]
            count = request.GET.get('count_'+goods_id)
            request_data.append((int(goods_id),int(count)))
    goodSet = set()
    show_data=[]
    total_price=0
    total_count=0
    for a in request_data:
        TheGood=good.objects.get(g_id=a[0])
        total_count+=a[1]
       
        
        aGood=newGood()
        
        aGood.goodName = TheGood.g_name
        aGood.goodUnite = '件'
        aGood.goodPrice = TheGood.g_price
        aGood.goodUrl = TheGood.g_picture
        aGood.goodId = TheGood.g_id
        aGood.goodAmount = a[1]
        aGood.goodTotalPrice = aGood.goodPrice * aGood.goodAmount
        total_price += aGood.goodTotalPrice
        goodSet.add(aGood)
        order.objects.create(u_id=int(request.session.get('u_id')),g_id=TheGood.g_id,o_number=a[1],price=aGood.goodTotalPrice,pay_status=-1)
        cart.objects.filter(userId=int(request.session.get('u_id')),g_id=TheGood.g_id).delete()
    if total_price>=50:
        transit_price=0
    else:
        transit_price=0
    total_pay=total_price-transit_price
    hasaddress=reciver.objects.filter(u_id=int(request.session.get('u_id'))).exists()
    if (hasaddress):
        curr_reciver=reciver.objects.get(u_id=int(request.session.get('u_id')))
    else:
        curr_reciver=None
    return render(request,'place_order1.html',{'list':goodSet,'total_count':total_count,'total_price':total_price,'transit_price':transit_price,'total_pay':total_pay,'hasaddress':hasaddress,'reciver':curr_reciver})
def endpay(request):
    uid=int(request.session.get('u_id'))
    orderlist=order.objects.filter(u_id=uid,pay_status=-1)
    hasgoods=1
    status=1
    if not (reciver.objects.filter(u_id=int(request.session.get('u_id')))).exists():
        order.objects.filter(u_id=uid,pay_status=-1).update(pay_status=0)
        msg='您没有默认地址'
        msg1='编辑地址'
        url='/user/addsite_show/'
        return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
    for o in orderlist:
        currgood=good.objects.get(g_id=o.g_id)
        print(currgood.g_total)
        print(o.o_number)
        if currgood.g_status==0:
            status=0
        if currgood.g_total<o.o_number:
            hasgoods=0
    if hasgoods==0:
        order.objects.filter(u_id=uid,pay_status=-1).update(pay_status=0)
        msg='库存不足'
        msg1='返回首页'
        url='/'
        return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
    if status==0:
        order.objects.filter(u_id=uid,pay_status=-1).update(pay_status=0)
        msg='商品已下架'
        msg1='返回首页'
        url='/'
        return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})
    order.objects.filter(u_id=uid,pay_status=-1).update(pay_status=1)


    msg='支付成功'
    msg1='返回首页'
    url='/'
    return render(request,'pay.html',{'msg':msg,'msg1':msg1,'url':url})