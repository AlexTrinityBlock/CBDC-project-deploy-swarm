from app_core.models.User import User
from app_core.services.ResolveRequest import ResolveRequest
from django.http import HttpResponse
import json

class GetUserPaymentID:
    def __init__(self):
        pass
    def get_user_payment_ID(self,request):        
        id = ResolveRequest.ResolveUserID(request)        
        bank_user_payment_id = User.objects.filter(id=id)[0].bank_user_payment_id
        return HttpResponse(json.dumps({
            "code":1,
            "bank_user_payment_id":bank_user_payment_id
        }))

