from app_core.services.ResolveRequest import ResolveRequest
import json
import requests
import os
from django.http import HttpResponse

class WithdrawProxy:
    def withdraw_proxy(self, request):
        data = ResolveRequest.ResolvePost(request)
        url = os.environ["USER_CRYPTOGRAPHY_SUPPORT_FLASK_SERVICE_URL"] + '/withdraw'
        result = requests.post(url, data=data).text
        return HttpResponse(result)