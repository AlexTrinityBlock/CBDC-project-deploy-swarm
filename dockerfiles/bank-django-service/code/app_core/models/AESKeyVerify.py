from django.db import models

# 商家的貨幣資料表
class AESKeyVerify(models.Model):
    user_id = models.CharField(max_length=100)
    aes_key_verify_ciphertext = models.CharField(max_length=100)
