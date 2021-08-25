from django.db import models
from django.utils.html import format_html
# Create your models here.
#创建商品类
class good(models.Model):
    g_name=models.CharField(verbose_name='商品名称',db_column='g_name',max_length=255) #商品名称
    g_price=models.DecimalField(verbose_name='商品价格',db_column='g_price',max_digits=10,decimal_places=2)
    g_picture=models.CharField(verbose_name='商品图片',db_column='g_picture',max_length=255)
    g_intro=models.CharField(verbose_name='商品简介',db_column='g_intro',max_length=500)
    g_id=models.IntegerField(verbose_name='商品id',db_column='g_id')
    t_id=models.IntegerField(verbose_name='商品类别id',db_column='t_id') #商品类别id
    uptime=models.DateTimeField(verbose_name='商品上架时间',db_column='uptime',auto_now_add=True) #商品上架时间，下架时间未用上暂时未写
    g_total=models.IntegerField(verbose_name='商品库存',db_column='g_total') #商品库存
    g_status=models.IntegerField(db_column='g_status')   
    def getTname(self):
        return type.objects.get(t_id=self.t_id).t_name
    def image_data(self):
        return format_html(
            '<img src="{}" width="40px"/>',
            self.g_picture,
        )
    image_data.short_description = '商品图片'
    getTname.short_description = '商品类别'

    class Meta:
        db_table='tb_goods'
        verbose_name = verbose_name_plural = '商品信息'

#创建类别类
class type(models.Model):
    t_id=models.IntegerField(db_column='t_id')
    t_status=models.IntegerField(db_column='t_status') #类别状态，暂时未用上
    t_name=models.CharField(db_column='t_name',max_length=255)
    class Meta:
        db_table='tb_type'