from collections import Set

from django.db.models import QuerySet
from django.http import JsonResponse, request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from good.views import detail
# Create your views here.
from django.views import View

from cart.models import cart
from good.models import good
from user.models import user

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
        message='已加入购物车'
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
