from django.db import models

# Create your models here.
class cart(models.Model):
    cartId=models.IntegerField(db_column='c_id')#购物车ID
    userId=models.IntegerField(db_column='u_id')#购物车的主人的ID
    g_id=models.IntegerField(db_column='g_id')#商品的ID
    goodAmount=models.IntegerField(db_column='c_number')#购物车里该商品的数量
    class Meta:
        db_table='tb_buycar'