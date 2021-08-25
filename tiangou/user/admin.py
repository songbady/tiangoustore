from django.contrib import admin
from django.utils import html
from user.models import *

# Register your models here.
#后台管理员网页管理显示，以及页面管理显示
admin.site.site_header = '天狗商城后台管理'
admin.site.index_title = '后台系统'
admin.site.site_title = '管理'
@admin.register(user)
class userAdmin(admin.ModelAdmin):
    #列表页显示的字段
    list_display = ['u_id','username','email','phone','ban']  
    #列表页的链接
    list_display_links = ['username']  
    #过滤的信息
    list_filter = ['ban']  
    #支持模糊搜索的选项
    search_fields = ['u_id','username','phone']
    #可在列表操作的信息
    list_editable = ['email','phone','ban']
    #分页功能
    list_per_page = 8