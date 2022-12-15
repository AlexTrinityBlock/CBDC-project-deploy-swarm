from django.db import models

# 使用者資料表
class User(models.Model):
    """使用者資料表
    未完成
    撰寫: 蕭維均
    """
    account = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=100)
    name = models.CharField(null=True,max_length= 100)
    home_address = models.CharField(null=True,default="Address",max_length=100)
    e_mail = models.CharField(null=True,max_length= 100)
    phone =models.CharField(null=True,default="09xxxxxxxx",max_length=100)
    bank_user_payment_id = models.CharField(null=True,max_length= 100)
