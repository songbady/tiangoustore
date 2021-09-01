
from django.db import models
from good.models import good

# Create your models here.
class order(models.Model):
    o_id=models.IntegerField(verbose_name='订单id',primary_key=True)
    u_id=models.IntegerField(verbose_name='用户id',db_column='u_id')
    time=models.DateTimeField(verbose_name='下单时间',db_column='time',auto_now=True)
    g_id=models.IntegerField(verbose_name='商品id',db_column='g_id')
    o_number=models.IntegerField(verbose_name='商品数量',db_column='o_number')
    price=models.DecimalField(verbose_name='订单价格',db_column='price',max_digits=10,decimal_places=2)
    pay_status=models.IntegerField(verbose_name='订单状态',db_column='pay_status')

    class Meta:
        db_table='tb_orderform'
        verbose_name = verbose_name_plural = '订单信息'
    def getGood(self):
        
        return good.objects.get(g_id=self.g_id)
        
