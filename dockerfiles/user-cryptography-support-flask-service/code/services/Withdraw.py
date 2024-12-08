import unittest
from flask import url_for, Flask
from flask_testing import TestCase
from services.YiModifiedPaillierEncryptionPy import YiModifiedPaillierEncryptionPy
from services.PartiallyBlindSignatureClientInterface import PartiallyBlindSignatureClientInterface
import requests
import os
import json
import uuid
import hashlib
import random

class Withdraw:
    def __init__(self):
        pass

    def hash(self, message:str):
        """Hash函數H()

        使用SHA256，Hash算法
        """
        h = hashlib.new('sha256')
        h.update(bytes(message, 'utf-8'))
        hex_string = h.hexdigest()
        return hex_string

    def withdraw(self,request):
        try:
            url = os.environ['BANK_DJANGO_SERVICE_URL']
            try:
                withdraw = request.form['withdraw']
                token = request.form['token']
            except Exception as e:
                return {
                    "code":0,
                    "Hint":"Fail to withdraw",
                    'error':str(e)
                }

            random_number =str(random.randint(0,9999999))
            secret_message = json.dumps({
                "uuid":self.hash(str(uuid.uuid4())+random_number)[:10],
                "text":"CBDC user"
            }) 

            signer_step1 = requests.post(url+"/api/blind-signature/step/1/get/K1/Q/bit-list", data={'token': token,'withdraw':withdraw}, timeout=3).text
            signer_step1_obj = json.loads(signer_step1)

            user= PartiallyBlindSignatureClientInterface()
            user.generate_message_hash(secret_message)
            user.generate_I(signer_step1_obj['PublicInfomation'])
            user.step1_input(signer_step1)
            user.generate_keypairs_parameters()
            user_step1 = user.step1_output()

            signer_step2 = requests.post(url+"/api/blind-signature/step/2/get/i-list", data={'token': token, 'data':user_step1}, timeout=3).text

            user.step3_input(signer_step2)
            user_step4 = user.step4_output()
            
            signer_step5 = requests.post(url+"/api/blind-signature/step/5/get/C", data={'token': token, 'data':user_step4}, timeout=3).text

            user.step5_input(signer_step5)

            result = dict()
            result['code'] = 1
            result['Hint'] = 'Success to withdraw'
            result['Info'] = signer_step1_obj['PublicInfomation']
            result['message'] = secret_message
            result['t'] = hex(user.t)
            result['s'] = hex(user.s)
            result['R'] = hex(user.R)
        except Exception as e:
            return {
                "code":0,
                "Hint":"Fail to withdraw",
                'error':str(e)
            }
        result =  json.dumps(result)
        # result = result.replace("\\", "")
        return result