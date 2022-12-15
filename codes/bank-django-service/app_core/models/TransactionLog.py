from django.db import models

class TransactionLog(models.Model):
   """
   交易紀錄資料表
   """
   user_id = models.IntegerField(null=True) # 與該次交易有關使用者ID
   status = models.IntegerField(null=True) # 狀態1或者0，1成功，0失敗。
   type = models.CharField(null=True,max_length=100) # 交易的型態，如提款存款
   used_currency = models.CharField(null=True,max_length=1000) # 若是存款，保留貨幣的內容。
   message = models.CharField(null=True,max_length=1000) # 額外訊息
   amount = models.IntegerField(null=True) # 提款的額度
   log_time = models.DateTimeField(auto_now=True)