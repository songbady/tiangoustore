from django.shortcuts import redirect, render
from good.models import*
from django.core.paginator import Paginator
import math
# Create your views here.
#显示首页
def index(request):
    #查询所有电脑类产品,取出前四个作为首页显示
    c_list=good.objects.filter(t_id=1)[0:4]
    
    #查询所有手机类商品,取出前四个作为首页显示
    p_list=good.objects.filter(t_id=2)[0:4]
    #查询男装类商品前四个，数据库暂时没添加数据
    #m_list=good.objects.filter(t_id=3)[0:4]
    #查询女装类商品前四个，数据库暂时没添加数据
    #p_list=good.objects.filter(t_id=4)[0:4]
    return render(request,'index.html',{'c_list':c_list,'p_list':p_list,'num':1,'tid1':1,'tid2':2,'tid3':3,'tid4':4})
#显示指定类的商品列表
def list(request,tid=1,num=1):
    if request.session.get('islogin')=='1':
        #对url传入参数转型
        tid=int(tid)
        num=int(num)
        #获取当前类别所有商品
        goodslist=good.objects.filter(t_id=tid)
        #获取类别名称
        tname=type.objects.get(t_id=tid).t_name
        Tid=tid

        #商品分页显示
        pager=Paginator(goodslist,1)
        #获取当前页面商品
        page_goodslist=pager.page(num)
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
       
        return render(request,'list.html',{'goodslist':page_goodslist,'Tid':Tid,'pagelist':pagelist,'tname':tname,'num':1,'tid1':1,'tid2':2,'tid3':3,'tid4':4})
    else:
        return redirect('/user/login/')
#显示商品详情
def detail(request,gid):
    if request.session.get('islogin')=='1':
        #参数转型
        gid=int(gid)
        #获取当前商品
        cur_good=good.objects.filter(g_id=gid).first()
        #获取商品类别名称
        tname=type.objects.get(t_id=cur_good.t_id).t_name
        #获取最近上架商品
        new_goodslist=good.objects.order_by('uptime')[0:2]
        return render(request,'detail.html',{'good':cur_good,'tid1':1,'tid2':2,'tid3':3,'tid4':4,'num':1,'tname':tname,'newgoods':new_goodslist})
    else :
        return redirect('/user/login/')