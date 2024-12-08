from app_core.models.TransactionLog import TransactionLog as TransactionLogModel
from app_core.services.ResolveRequest import ResolveRequest
from app_core.services.UUIDRandom import UUIDRandom
from app_core.models.User import User
from app_core.models.UserBalance import UserBalance
from django.http import HttpResponse
import json
import os
from datetime import datetime

class TransactionLog:
    def transaction_log(self,request):
        # 取得角色資訊
        role = ResolveRequest.ResolveRole(request)
        # 若沒有使用者權限，則無法生成
        if role != 'administrator': 
            return HttpResponse(json.dumps({
                'code': 0,
                'message': 'User forbidden'
        }))

        transaction_logs = TransactionLogModel.objects.all()
        transaction_logs_list = list()

        for transaction_log in transaction_logs:
            transaction_log_dict = dict()
            transaction_log_dict['id'] = transaction_log.id
            transaction_log_dict['user_id'] = transaction_log.user_id 
            transaction_log_dict['status'] = transaction_log.status
            transaction_log_dict['type'] = transaction_log.type
            transaction_log_dict['used_currency'] = transaction_log.used_currency
            transaction_log_dict['message'] = transaction_log.message
            transaction_log_dict['amount'] = transaction_log.amount
            transaction_log_dict['log_time'] = transaction_log.log_time.strftime("%Y/%m/%d  %H:%M:%S")
            transaction_logs_list.append(transaction_log_dict)

        return HttpResponse(json.dumps({
            'code': 1,
            'transaction_logs': json.dumps(transaction_logs_list)
        }))