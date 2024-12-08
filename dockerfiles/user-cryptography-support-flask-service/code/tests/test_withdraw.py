# docker-compose exec user-cryptography-support-flask-service bash
import unittest
from flask import url_for, Flask
from flask_testing import TestCase
from services.YiModifiedPaillierEncryptionPy import YiModifiedPaillierEncryptionPy
from services.PartiallyBlindSignatureClientInterface import PartiallyBlindSignatureClientInterface
import requests
import os
import json
from services.VerifyCurrency import VerifyCurrency

class TestAlgorithm(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        print("\n=================")
 
      # 在結束測試時會被執行
    def tearDown(self):
        print("=================")

    def test_withdraw(self):
        print("提款測試")

        url = os.environ['BANK_DJANGO_SERVICE_URL']
        result = requests.post(url+"/api/login", data={'account': 'user', 'password':'user'}, timeout=3).text
        token = json.loads(result)['token']

        local = "http://127.0.0.1:5000"
        result = requests.post(local+"/withdraw", data={'token': token,'withdraw':1}, timeout=3).text
        
        signature = json.loads(result)

        print(signature)

        t = int(signature['t'],16)
        s = int(signature['s'],16)
        R = int(signature['R'],16)
        verifyCurrency = VerifyCurrency()
        result = verifyCurrency.verify_currency(t,s,R,signature['message'],signature['Info'])
        self.assertEqual(result,True)


