from django.db import models

# 商家的貨幣資料表
class DigitalWallet(models.Model):
    user_id = models.CharField(max_length=100)
    encrypted_currency = models.CharField(max_length=1000)