
from django.db import models
from good.models import good

# Create your models here.
class order(models.Model):
    o_id=models.IntegerField(db_column='o_id')
    u_id=models.IntegerField(db_column='u_id')
    time=models.DateTimeField(db_column='time',auto_now=True)
    g_id=models.IntegerField(db_column='g_id')
    o_number=models.IntegerField(db_column='o_number')
    price=models.DecimalField(db_column='price',max_digits=10,decimal_places=2)
    pay_status=models.IntegerField(db_column='pay_status')
    class Meta:
        db_table='tb_orderform'
    def getGood(self):
        
        return good.objects.get(g_id=self.g_id)
