from app_core.models.Voucher import Voucher as VoucherModel
from app_core.services.ResolveRequest import ResolveRequest
from app_core.services.UUIDRandom import UUIDRandom
from app_core.models.User import User
from app_core.models.UserBalance import UserBalance
from app_core.models.TransactionLog import TransactionLog
from django.http import HttpResponse
import json
import os

class Voucher:
    def __init__(self):
        pass
    def generate_voucher(self,request):
        """
        用管理員帳戶生成代金券
        """
        role = ResolveRequest.ResolveRole(request)
        data = ResolveRequest.ResolvePost(request)
        # 若沒有使用者權限，則無法生成
        if role != 'administrator': 
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'User forbidden'
        }))
        token =UUIDRandom.random_uuid_string()[:int(os.environ['BANK_VOUCHER_LENGTH'])]
        voucher = VoucherModel()
        voucher.currency = data['amount']
        voucher.voucher_token = token
        voucher.save()

        # 進行交易紀錄
        transaction_log_model = TransactionLog()
        transaction_log_model.status = 1
        transaction_log_model.amount = data['amount']
        transaction_log_model.type = 'Administrator issue voucher.'
        transaction_log_model.message = 'Administrator issue voucher $'+ str(data['amount']) + '.'
        transaction_log_model.save()

        return HttpResponse(json.dumps({
            'code': 1,
            'token': token
        }))

    def redeem_voucher(self,request):
        # 輸入資料擷取
        input_data = ResolveRequest.ResolvePost(request)
        input_voucher_token = input_data['voucher_token']
        
        # 取得點數卡資料庫實例
        voucher = VoucherModel.objects.filter(voucher_token=input_voucher_token)

        # 檢查Token是否有效
        if voucher.count() != 1:
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'Invalid voucher token'
            }))

        # 檢查點數卡是否被使用過
        if voucher[0].is_used == 1:
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'Voucher token is used'
            }))

        # 取得該點數卡的餘額
        currency_in_voucher = voucher[0].currency

        # 設置點數卡為已經使用過了
        voucher = voucher[0]
        voucher.is_used = 1
        voucher.save()

        # 更新貨幣總數
        user_id = ResolveRequest.ResolveUserID(request)
        user_balance = UserBalance.objects.filter(user_id=user_id)[0]
        user_balance.balance = user_balance.balance + currency_in_voucher
        user_balance.save()
        
        # 進行交易紀錄
        transaction_log_model = TransactionLog()
        transaction_log_model.used_currency = input_data['voucher_token']
        transaction_log_model.user_id =  ResolveRequest.ResolveUserID(request)
        transaction_log_model.status = 1
        transaction_log_model.amount = currency_in_voucher
        transaction_log_model.type = 'User redeem voucher!'
        transaction_log_model.message = 'Success get $'+str(currency_in_voucher)
        transaction_log_model.save()

        return HttpResponse(json.dumps({
            'code': 1,
            'message': 'The voucher successfully deposited into the bank'
        }))

    # 列出代金券
    def list_voucher(self,request):
        """
        用管理員帳戶生成代金券
        """
        role = ResolveRequest.ResolveRole(request)

        # 若沒有使用者權限，則無法生成
        if role != 'administrator': 
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'User forbidden'
        }))

        vouchers = VoucherModel.objects.all()
        voucher_list = list()

        for voucher in vouchers:
            voucher_dict = dict()
            voucher_dict['id'] = voucher.id
            voucher_dict['currency'] = voucher.currency
            voucher_dict['voucher_token'] = voucher.voucher_token
            voucher_dict['is_used'] = voucher.is_used
            voucher_list.append(voucher_dict)

        return HttpResponse(json.dumps({
            'code': 1,
            'vouchers': json.dumps(voucher_list)
        }))
