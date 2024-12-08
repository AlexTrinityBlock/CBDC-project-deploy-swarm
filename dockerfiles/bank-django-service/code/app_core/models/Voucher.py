from django.db import models

# 使用者資料表
class Voucher(models.Model):
    """代金券(點數卡)資料表
    可以換成存款的點數卡序號
    """
    currency = models.IntegerField()
    voucher_token = models.CharField(max_length=100)
    is_used = models.IntegerField(default=0)
