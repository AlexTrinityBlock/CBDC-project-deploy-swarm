from django.test import TestCase
from app_core.models.User import User
from django.test.client import RequestFactory
from app_core.services.Register import Register
import json

class TestRegist(TestCase):
    def setUp(self):
        pass
    def test_register(self):
        
        print("[註冊測試] 註冊測試判別。")

        rf = RequestFactory()
        post_request = rf.post('/api/register/', {'account': 'test1sdfds1w23ewq', 'password':'test','e_mail':'test@example.com','user_name':'Test User name','phone':'000000000','home_address':'Address'})

        register = Register()
        response = register.register(post_request) 
        result = json.loads(response.content.decode("utf-8"))
        self.assertEqual(result['code'], 1)

        user_number = User.objects.filter(account='test1sdfds1w23ewq').count()
        self.assertEqual(user_number, 1)