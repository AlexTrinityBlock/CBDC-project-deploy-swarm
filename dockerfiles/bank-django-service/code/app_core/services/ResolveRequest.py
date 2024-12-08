import os
import redis
import json
from app_core.models.User import User

class ResolveRequest:
    def __init__(self):
        pass
    
    @staticmethod
    def ResolveToken(request):
        # 無論GET或者POST都接收，之後依照需求修改
        if request.method == 'GET':
            data = request.GET
        elif request.method == 'POST':
            data = request.POST

        # 檢查Token 是否正確，同時相容token存在於cookie或者request中。
        if "token" in data:
            token = data["token"]
        elif "token" in request.COOKIES:
            token = request.COOKIES["token"]

        return token

    @staticmethod
    def ResolveGet(request):
        if request.method == 'GET':
            return request.GET
        else:
            raise Exception("方法錯誤")

    @staticmethod
    def ResolvePost(request):
        if request.method == 'POST':
            return request.POST
        else:
            raise Exception("方法錯誤")

    @staticmethod
    def ResolveRole(request):
        redis_connection = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        token = ResolveRequest.ResolveToken(request)
        data = json.loads(redis_connection.get(token))
        return data['role']

    @staticmethod
    def ResolveUserID(request) -> int:
        redis_connection = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        token = ResolveRequest.ResolveToken(request)
        data = json.loads(redis_connection.get(token))
        account = data['account']
        id = User.objects.filter(account=account)[0].id
        return id
