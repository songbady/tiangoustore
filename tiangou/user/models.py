from django.db import models

# Create your models here.
class user(models.Model):
    u_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    #ur_id = models.IntegerField()
    ban = models.TextField()  # This field type is a guess.
    del_flag = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tb_user'
class user(models.Model):
    u_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    ban = models.TextField()  # This field type is a guess.
    del_flag = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tb_user'