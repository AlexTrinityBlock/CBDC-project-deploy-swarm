from django.test import TestCase
from app_core.services.Login import Login
from app_core.models.User import User
from django.test.client import RequestFactory
import redis
import requests
import json
import os


class TestLogin(TestCase):
    """測試登入系統
    確認登入系統是否正常
    """
    # 測試初始設置
    def setUp(self):
        # 網址路徑
        self.login_url = 'http://localhost:8000/api/login'
        self.check_login_url = 'http://localhost:8000/api/check_login'
        # 使用者帳號與密碼的Hash
        self.account = "user"
        self.password = 'user'
        self.password_hash = "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb"
        # 建立測試用使用者資料
        User.objects.create(account = self.account)
        User.objects.create(password_hash = self.password_hash)
        # 建立 Redis 連線
        self.redis_connection_token_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        self.redis_connection_user_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=1, password=os.environ['REDIS_PASSWORD'])
        
    # 測試登入
    def test_Login(self):
        pass