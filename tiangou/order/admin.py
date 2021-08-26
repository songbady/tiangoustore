from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import reverse
from order.models import *
# Register your models here.
@admin.register(order)

class orderAdmin(admin.ModelAdmin):
    #列表显示的字段
    list_display = ['u_id','o_id','time','g_id','o_number','pay_status','price','operator']
   #列表页的链接
    list_display_links = ['o_id','u_id']
    #支持模糊搜索的选项
    search_fields = ['o_id','u_id']
    #可在列表操作的信息
    list_editable = ['o_number']
     #过滤的信息
    list_filter = ['time','g_id'] 
    #分页功能
    list_per_page = 8

    def operator(self,obj):
        #change_href=reverse('admin:order_order_change',args=(obj.id,))
        delete_href=reverse('admin:order_order_delete',args=(obj.id,))
        html='<a style="color:deepskyblue;"href="%s">删除</a>'%(delete_href)
        
        return format_html(html)

    operator.short_description="操作"
    