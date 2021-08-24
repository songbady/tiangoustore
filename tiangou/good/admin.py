from django.contrib import admin
from django.utils.html import format_html
from good.models import *
# Register your models here.
@admin.register(good)

class goodAdmin(admin.ModelAdmin):
    #列表显示的字段
    list_display = ['g_id','g_name','t_id','getTname','image_data','g_price','g_total','uptime']
    #列表页的链接
    list_display_links = ['g_id','g_name']  
    #过滤的信息
    list_filter = ['t_id','g_price','uptime']  
    #支持模糊搜索的选项
    search_fields = ['g_id','g_name','t_id']
    #可在列表操作的信息
    list_editable = ['g_price','g_total']

