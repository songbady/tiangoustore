from django.db import models

# Create your models here.
#创建商品类
class good(models.Model):
    g_name=models.CharField(db_column='g_name',max_length=255) #商品名称
    g_price=models.DecimalField(db_column='g_price',max_digits=10,decimal_places=2)
    g_picture=models.CharField(db_column='g_picture',max_length=255)
    g_intro=models.CharField(db_column='g_intro',max_length=500)
    g_id=models.IntegerField(db_column='g_id')
    t_id=models.IntegerField(db_column='t_id') #商品类别id
    uptime=models.DateTimeField(db_column='uptime',auto_now_add=True) #商品上架时间，下架时间未用上暂时未写
    g_total=models.IntegerField(db_column='g_total') #商品库存
    def getTname(self):
        return type.objects.get(t_id=self.t_id).t_name
    class Meta:
        db_table='tb_goods'
#创建类别类
class type(models.Model):
    t_id=models.IntegerField(db_column='t_id')
    t_status=models.IntegerField(db_column='t_status') #类别状态，暂时未用上
    t_name=models.CharField(db_column='t_name',max_length=255)
    class Meta:
        db_table='tb_type'