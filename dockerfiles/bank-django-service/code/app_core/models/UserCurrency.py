from django.db import models

# 顧客的貨幣資料表
class UserCurrency(models.Model):
    user_id = models.CharField(default="user_id",max_length=100)
    denomination =models.IntegerField(default=0)
    coin_seq= models.CharField(default="coin_seq",max_length=100)
    sign_coin_seq = models.CharField(default="sign_coin_seq",max_length=100)
    spend_check =models.BooleanField(default=False)
    