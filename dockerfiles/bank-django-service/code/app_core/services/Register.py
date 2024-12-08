from django.http import HttpResponse
from app_core.models.User import User
from app_core.models.UserBalance import UserBalance
from app_core.services.UUIDRandom import UUIDRandom
import hashlib

import json 

class Register():
    def register(self,request):
        # 無論GET或者POST都接收，之後依照需求修改
        if request.method == 'GET':
            result = {'code':0, 'message':'Registe post required'}
            result = json.dumps(result)
            return HttpResponse(result)
        elif request.method == 'POST':
            data = request.POST
        password = data['password']
        password = password.encode('utf-8')
        password_hash = hashlib.sha256(password).hexdigest()
        user = User()
        user_account_number = User.objects.filter(account=data['account']).count() #數帳號
        print(user_account_number)
        if(user_account_number>0): 
            result = {'code':2, 'message':'account is created'}
            result = json.dumps(result)
            return HttpResponse(result)

        try:
            user.account = data['account']
            user.e_mail = data['e_mail']
            user.password_hash = password_hash
            user.name = data['user_name']
            user.phone = data['phone']
            user.home_address = data['home_address']
            user.bank_user_payment_id = UUIDRandom.random_uuid_string()
            user.save()
        except:
            result = {'code':0, 'message':'Missing parameters!'}
            result = json.dumps(result)
            return HttpResponse(result)
        # 新增帳戶時添加一個存款資料表條目。
        user_id = User.objects.filter(account=data['account'])[0].id
        user_balance = UserBalance()
        user_balance.user_id = user_id
        user_balance.save()

        result = {'code':1, 'message':'registe success.'}
        result = json.dumps(result)
        return HttpResponse(result)