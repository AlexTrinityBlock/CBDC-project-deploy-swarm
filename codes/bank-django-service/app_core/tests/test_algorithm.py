from django.test import TestCase
import os
import json
from pprint import pprint
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey, PublicKey
from app_core.services.YiModifiedPaillierEncryptionPy import YiModifiedPaillierEncryptionPy
from app_core.services.PartiallyBlindSignatureClientInterface import PartiallyBlindSignatureClientInterface
from app_core.services.PartiallyBlindSignatureServerInterface import PartiallyBlindSignatureServerInterface
from app_core.services.Login import Login
import requests
import redis
import gmpy2

class TestAlgorithm(TestCase):
    
    def setUp(self):
        self.ECDSA_PUBLICKEY = os.environ['ECDSA_PUBLICKEY']
        self.ECDSA_PRIVATEKEY = os.environ['ECDSA_PRIVATEKEY']
        pass

    # 測試Yi算法
    def test_YiModifiedPaillierEncryptionPy(self):
        print("[算法測試] 測試Yi同態加密")
        yiModifiedPaillierEncryptionPy = YiModifiedPaillierEncryptionPy()
        yiModifiedPaillierEncryptionPy.test()

    # 測試ECDSA模塊
    def test_ECDSA(self):
        print("[算法測試] ECDSA模塊")
        privateKey = PrivateKey.fromPem(self.ECDSA_PRIVATEKEY)
        publicKey = PublicKey.fromPem(self.ECDSA_PUBLICKEY)
        message = json.dumps({"data": "123"})
        signature = Ecdsa.sign(message, privateKey)
        result = Ecdsa.verify(message, signature, publicKey)
        self.assertTrue(result, "\n\n ECDSA模塊測試失敗，有可能是模塊損壞或者ECDSA鑰匙錯誤")

    def test_PartiallyBlindSignatureServerInterface(self):
        print("[算法測試] 盲簽章算法驗證")
        redis_connection_0 = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD']) 
        redis_connection_1 = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=1, password=os.environ['REDIS_PASSWORD']) 

        login = Login()
        token = login.setUserToken("user")

        signer = PartiallyBlindSignatureServerInterface(token)
        signer.generate_I("Public")
        signer_step1 = signer.output()
        signer.save_and_next_step(token)
        # print(signer.K1x)
        # print(signer.ECDSA_PRIVATEKEY)
        # print("簽署者將公鑰傳遞給使用者，並且將零知識證明的提問順便傳送")
        # pprint(signer_step1)
        # print("")

        user = PartiallyBlindSignatureClientInterface()
        user.generate_message_hash("Message")
        user.generate_I("Public")
        user.step1_input(signer_step1)
        user.generate_keypairs_parameters()
        user_step1 = user.step1_output()
        # print("使用者將 C1, C2, 零知識證明內容，F1~Fn傳送給簽署者")
        # pprint(user_step1)
        # print("")

        signer.input(user_step1)
        signer.save_and_next_step(token)
        signer_step3 = signer.output()
        signer.save_and_next_step(token)
        # print("簽署者將i序列傳給使用者")
        # pprint(signer_step3)
        # print("")
        
        user.step3_input(signer_step3)
        use_step4_output = user.step4_output()
        # print("使用者將對應的L傳給簽署者")
        # pprint(use_step4_output)
        # print("")

        signer.input(use_step4_output)
        signer.save_and_next_step(token)
        signer_step5 = signer.output()

        user.step5_input(signer_step5)

        redis_connection_0.delete(token)
        redis_connection_1.delete('user')

        self.assertEqual(user.t,user.t_p)