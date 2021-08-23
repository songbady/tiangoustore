from django.contrib import admin
from django.utils import html
from user.models import *
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.
admin.site.site_header = '天狗商城后台管理'
admin.site.index_title = '后台系统'
admin.site.site_title = '管理'
@admin.register(user)
class userAdmin(admin.ModelAdmin):
     list_display = ['u_id','username','password','email','phone']#,'operator']
     list_filter = ['ban']
     search_fields = ['u_id','username','phone']

    #  def operator(self,obj):
    #      change_href:reverse('admin:user_user_change',args=(obj.id,))
    #      delete_href:reverse('admin:user_user_delete',args=(obj.id,))
    #      html = '<a style="color:deepskyblue;"href="%s">编辑</a>&#12288;<a style="color:palevioletred;"href="%s">删除</a>' % (change_href,delete_href)
    #      return format_html(html)
    #  operator.short_description ='操作'
    #  def operator(self, obj):
    #     return format_html(
    #         '<a href="{}">编辑</a>',
    #         reverse('admin:user_user_change', args=(obj.id,))
    #     )
    #  operator.short_description = '操作