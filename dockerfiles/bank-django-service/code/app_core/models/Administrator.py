from django.db import models

# 使用者資料表
class Administrator(models.Model):
    """使用者資料表
    未完成
    撰寫: 蕭維均
    """
    account = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=100)
    access_control_list = models.CharField(null=True,max_length=1000)
