from app_core.services.ResolveRequest import  ResolveRequest
from app_core.models.UserBalance import UserBalance
from django.http import HttpResponse
import json

class GetBalance:
    """
    獲取使用者餘額的服務
    """
    def get_balance(self,request):
        data = ResolveRequest.ResolveGet(request)
        id = ResolveRequest.ResolveUserID(request)
        balance = UserBalance.objects.filter(user_id=id)[0].balance

        return HttpResponse(json.dumps({
            'balance': balance,
            'code':1,
        }))