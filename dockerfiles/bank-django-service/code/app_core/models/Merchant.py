from django.db import models

# 商家的貨幣資料表
class Merchant(models.Model):

    name = models.CharField(default="Name",max_length=100)
    address = models.CharField(default="Address",max_length=100)
    owner = models.CharField(default="Owner",max_length=100)
    phone = models.CharField(default="05xxxxxxx",max_length=100)
    remaining = models.IntegerField(default=0)