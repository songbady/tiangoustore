from django.db import models

# Create your models here.
class users(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    email=models.EmailField(max_length=50)
    phone=models.CharField(max_length=11)
    