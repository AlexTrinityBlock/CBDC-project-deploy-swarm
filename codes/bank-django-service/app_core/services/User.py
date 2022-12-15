from app_core.services.ResolveRequest import ResolveRequest
from django.http import HttpResponse
import json
import os
import redis

class User:
    def __init__(self):
        pass
    def get_account(self,request):
            redis_connection = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
            token = ResolveRequest.ResolveToken(request)
            data = json.loads(redis_connection.get(token))
            account = data['account']
            return HttpResponse(json.dumps({
                "account": account,
                "code":1
            }))