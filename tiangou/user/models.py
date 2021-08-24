from django.db import models

# Create your models here.
class user(models.Model):
    STATE_ITEM = (
        (0,'启动'),
        (1,'禁用'),
    )
    u_id = models.AutoField(verbose_name='用户id',primary_key=True)
    username = models.CharField(verbose_name='用户姓名',max_length=32)
    password = models.CharField(verbose_name='用户密码',max_length=64)
    email = models.CharField(verbose_name='电子邮箱',max_length=50, blank=True, null=True)
    phone = models.CharField(verbose_name='电话',max_length=11, blank=True, null=True)
    ur_id = models.IntegerField()
    ban =  models.PositiveSmallIntegerField(default=0,verbose_name='状态',choices=STATE_ITEM)
    del_flag = models.TextField()  # This field type is a guess.

    class Meta:
        #managed = False
        db_table = 'tb_user'
        verbose_name = verbose_name_plural = '用户信息'