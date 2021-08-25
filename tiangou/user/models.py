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
    ban = models.PositiveIntegerField(default=0,verbose_name='状态',choices=STATE_ITEM)
    #ban =  models.PositiveSmallIntegerField(default=0,verbose_name='状态',choices=STATE_ITEM)
    del_flag = models.TextField()  # This field type is a guess.

    class Meta:
        #managed = False
        db_table = 'tb_user'
        verbose_name = verbose_name_plural = '用户信息'
class reciver(models.Model):
    r_id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(db_column="u_id")
    r_name = models.CharField("收件人", max_length=20,db_column="r_name")
    r_province=models.CharField("省份",max_length=10,default="北京",db_column='r_province')
    r_city=models.CharField("城市",max_length=10,default="北京",db_column='r_city')
    r_district=models.CharField("区/县",max_length=10,default="朝阳区",db_column='r_district')
    r_address = models.CharField("具体地址", max_length=50,default="xxx小区",db_column='r_address')  # 家，公司，学校等
    r_phone = models.CharField("手机号", max_length=12, default="13333333333",db_column='r_phone')
    #is_default = models.BooleanField("是否为默认地址", default=False)
    r_zipcode = models.CharField("邮编", max_length=6, default="000000",db_column='r_zipcode')
    createtime=models.DateTimeField(db_column='createtime',auto_now=True)
    class Meta:
        db_table = 'tb_reciver'
        verbose_name = '地址'
        verbose_name_plural = verbose_name  