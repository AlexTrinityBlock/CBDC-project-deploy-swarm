from tokenize import Token
from app_core.models.User import User
import hashlib
import json 
import redis
import os
import uuid
from django.http import HttpResponse

class Login():
    """登入類別
    撰寫: 蕭維均
    """
    def check_account(self, account:str):
        user_exist =  User.objects.filter(account=account).count()
        return True if user_exist == 1 else False

    def check_password(self,account:str ,password:str):
        password = password.encode('utf-8')
        password_hash = hashlib.sha256(password).hexdigest()
        result = User.objects.filter(account = account, password_hash = password_hash).count()
        return True if result == 1 else False

    def setUserToken(self,account:str):
        # 生成Token 
        token = uuid.uuid4().hex
        json_data = json.dumps({
            'account':account,
            'role':'user'
        })
        
        # Redis 連線物件
        redis_connection_token_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        redis_connection_user_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=1, password=os.environ['REDIS_PASSWORD'])

        # 檢查使用者是否在已經登入的用戶表中，終止後續程序，回傳Token
        if redis_connection_user_index.exists(account):
            return redis_connection_user_index.get(account).decode("utf-8") 

        # 將使用者加入已經登入的使用者表單
        redis_connection_user_index.set(account,token)
        redis_connection_user_index.expire(account,1800)

        # 用 uuid 作為使用者的Token
        redis_connection_token_index.set(token,json_data)
        redis_connection_token_index.expire(token,1800) # 300 秒，5分鐘超時。

        return token

    # 登入方法
    def login(self, request):
        data = None
        result =dict()

        # 無論GET或者POST都接收，之後依照需求修改
        if request.method == 'GET':
            result = {'code':0, 'message':'Post method required.'}
            result = json.dumps(result)
            return HttpResponse(result)
        elif request.method == 'POST':
            # 適應不同的Fetch POST 實現
            try:
                data = json.loads(request.body)
            except:
                data = request.POST
            
        # 檢查 Requests 參數是否正確
        try:
            account = data['account']
            password = data["password"]
        except:
            result = {'code':0, 'message':'Login format wrong.'}
            result = json.dumps(result)
            return HttpResponse(result)

        # 檢查帳號密碼是否存在 
        if self.check_account(account):
            if self.check_password(account, password):
                # 檢查是否已經從別瀏覽器登入
                redis_connection_user_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=1, password=os.environ['REDIS_PASSWORD'])
                redis_connection_token_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
                # 若已經從別處登入
                if redis_connection_user_index.exists(account):
                   # 登出另一處
                    token = redis_connection_user_index.get(account)
                    redis_connection_user_index.delete(account)
                    redis_connection_token_index.delete(token)
                # 建立回應訊息
                result = {'code':1, 'message':'Login success.'}
                uuid_token = self.setUserToken(account)
                result["token"] = uuid_token
                result = json.dumps(result)
                result = HttpResponse(result)
                result.set_cookie('token',uuid_token,httponly=True)
                return result
            else:
                result = {'code':0, 'message':'Login fail.'}
        else:
            result = {'code':0, 'message':'Login fail.'}

        result = json.dumps(result)
        return HttpResponse(result)

    # 檢查是否登入
    def check_login(self, request):
        data = None
        result =dict()
        token = None

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
        elif token == None:# 若無token 進行回應
            result = {'code':0,'message':'Missing token'}
            result = json.dumps(result)
            return HttpResponse(result)

        # 檢查 Redis 中是否存在該Token
        if self.login_verify(token):
            result = {'code':1,'message':'Login success.'}
            result = json.dumps(result)
            result = HttpResponse(result)
            return result
        else:
            result = {'code':0,'message':'Login fail.'}
            result = json.dumps(result)
            return HttpResponse(result)


    # 檢查是否登入
    def check_login_from_request(self, request):
        data = None
        result =dict()
        token = None

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
        elif token == None:# 若無token 進行回應
            return False

        # 檢查 Redis 中是否存在該Token
        if self.login_verify(token):
            return True
        else:
            return False

    # 檢查是否登入(用於非API)的驗證
    def login_verify(self,token):
        redis_connection = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        if redis_connection.exists(token):
            return True
        else:
            return False

    # 登出
    def logout(self,request):
        redis_connection_token_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        redis_connection_user_index = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=1, password=os.environ['REDIS_PASSWORD'])
        # 只接收POST
        if request.method == 'GET':
            result = {'code':0, 'message':'Post method required.'}
            result = json.dumps(result)
            return HttpResponse(result)
        elif request.method == 'POST':
            # 適應不同的Fetch POST 實現
            try:
                data = json.loads(request.body)
            except:
                data = request.POST

        # 檢查Token 是否正確，同時相容token存在於cookie或者request中。
        if "token" in data:
            token = data["token"]
        elif "token" in request.COOKIES:
            token = request.COOKIES["token"]
        elif token == None:# 若無token 進行回應
            return False

        user = json.loads(redis_connection_token_index.get(token))['account']
        redis_connection_user_index.delete(user)
        redis_connection_token_index.delete(token)

        result = {'code':1,'message':'Logout success.'}
        result = json.dumps(result)
        return HttpResponse(result)