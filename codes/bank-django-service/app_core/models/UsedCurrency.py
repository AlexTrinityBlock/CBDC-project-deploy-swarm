from django.db import models

# 銀行簽章過的貨幣資料表
class UsedCurrency(models.Model):
    message = models.CharField(max_length=500)
    Info = models.CharField(max_length=100)
    R = models.CharField(max_length=100)
    s = models.CharField(max_length=100)
    t = models.CharField(max_length=100)