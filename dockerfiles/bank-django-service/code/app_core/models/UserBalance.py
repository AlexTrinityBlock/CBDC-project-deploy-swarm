from django.db import models

# 貨幣資料表
class UserBalance(models.Model):
    """貨幣資料表
    尚未完成
    撰寫: 蕭維均
    """
    user_id = models.IntegerField()
    balance = models.IntegerField(default=0)