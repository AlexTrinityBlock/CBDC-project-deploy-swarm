from django.http import HttpResponse
import json 
from app_core.services.PartiallyBlindSignatureServerInterface import PartiallyBlindSignatureServerInterface
from app_core.services.ResolveRequest import ResolveRequest
from app_core.models.UserBalance import UserBalance
from app_core.models.TransactionLog import TransactionLog
import redis
import os

class PartiallyBlindSignature:
    def __init__(self):
        pass

    def init_blind_signature(self,request):
        token = ResolveRequest.ResolveToken(request)
        self.redis_connection = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD']) 
        status = json.loads(self.redis_connection.get(token))
        del status['BlindSignature']
        self.redis_connection.set(token,json.dumps(status))
        self.redis_connection.expire(token, 18000)
        return HttpResponse(json.dumps({
            "code": 1,
            "message": "Refresh Signature status"
        }))

    def check_user_balance(self,request):
        """
        檢查使用者餘額是否足夠
        """
        withdraw = int(ResolveRequest.ResolvePost(request)['withdraw'])
        user_id = ResolveRequest.ResolveUserID(request)
        balance= UserBalance.objects.filter(user_id=user_id)[0].balance
        if withdraw > balance:
            return False
        else:
            return True

    def cost_user_balance(self,request,withdraw:int):
        user_id = ResolveRequest.ResolveUserID(request)
        user_balance = UserBalance.objects.filter(user_id=user_id)[0]
        user_balance.balance = user_balance.balance - withdraw
        user_balance.save()

    def api_blind_signature_step_1_get_K1_Q_bit_list(self,request):
        try:
            token = ResolveRequest.ResolveToken(request)
            self.server = PartiallyBlindSignatureServerInterface(token)

            # 檢查餘額
            if not self.check_user_balance(request):
                print('餘額不足')
                return HttpResponse(json.dumps({
                    'code':0,
                    'message':'Balance not enough!'
                }))

            # 把使用者提款額度押入盲簽章公開訊息
            withdraw = ResolveRequest.ResolvePost(request)['withdraw'] #取得使用者請求提款的額度            
            public_info = json.dumps({
                "currency":withdraw,
                "Text":"CBDC Bank."
            }) 
            self.server.generate_I(public_info)

            # 將使用者存款額度暫存到 Redis 中
            self.server.status['withdraw'] = withdraw
            
            result = self.server.output()
            self.server.save_and_next_step(token)
            return HttpResponse(result)
        except:
            self.init_blind_signature(request)
            return HttpResponse(json.dumps({
                "code": 0,
                "message": "step1 fail"
            }))        

    def api_blind_signature_step_2_get_i_list(self,request):
        try:
            token = ResolveRequest.ResolveToken(request)
            self.server = PartiallyBlindSignatureServerInterface(token)
            data = ResolveRequest.ResolvePost(request)['data']
            self.server.input(data)
            self.server.save_and_next_step(token)
            result = self.server.output()
            self.server.save_and_next_step(token)
            return HttpResponse(result)
        except:
            self.init_blind_signature(request)
            return HttpResponse(json.dumps({
                "code": 0,
                "message": "step2 fail"
            }))   

    def api_blind_signature_step_5_get_C(self,request):
        try:
            # 生成加密簽章
            token = ResolveRequest.ResolveToken(request)
            self.server = PartiallyBlindSignatureServerInterface(token)
            data = ResolveRequest.ResolvePost(request)['data']
            self.server.input(data)
            self.server.save_and_next_step(token)        
            result = self.server.output()
            self.init_blind_signature(request)
            
            # 扣款
            withdraw = int(self.server.status['withdraw'])
            self.cost_user_balance(request,withdraw)
            
            # 在順利完成前進行紀錄
            transaction_log_model = TransactionLog()
            transaction_log_model.user_id =  ResolveRequest.ResolveUserID(request)
            transaction_log_model.status = 1
            transaction_log_model.type = 'Withdraw'
            transaction_log_model.message = 'Success Withdraw !'
            transaction_log_model.amount = self.server.status['withdraw']
            transaction_log_model.save()

            return HttpResponse(result)
        except:
            # 對交易失敗進行紀錄
            transaction_log_model = TransactionLog()
            transaction_log_model.user_id =  ResolveRequest.ResolveUserID(request)
            transaction_log_model.status = 0
            transaction_log_model.type = 'Withdraw'
            transaction_log_model.message = 'Fail to Withdraw !'
            transaction_log_model.amount = self.server.status['withdraw']
            transaction_log_model.save()

            # 重置盲簽章狀態
            self.init_blind_signature(request)
            # 回傳失敗訊息
            return HttpResponse(json.dumps({
                "code": 0,
                "message": "step5 fail"
            }))   