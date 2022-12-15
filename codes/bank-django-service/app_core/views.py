from django.shortcuts import render
from django.http import HttpResponse
from app_core.services.Login import Login
from app_core.services.AdministratorLogin import AdministratorLogin
from app_core.services.Register import Register
from app_core.services.PartiallyBlindSignaturePublicParameters import PartiallyBlindSignaturePublicParameters
from app_core.services.PartiallyBlindSignature import PartiallyBlindSignature
from app_core.services.Voucher import Voucher
from app_core.services.RedeemCurrency import RedeemCurrency
from app_core.services.GetBalance import GetBalance
from app_core.services.GetUserPaymentID import GetUserPaymentID
from app_core.services.AesVerifyKey import AesVerifyKey
from app_core.services.User import User
from app_core.services.ResolveRequest import ResolveRequest
from app_core.services.WithdrawProxy import WithdrawProxy
from app_core.services.TransactionLog import TransactionLog
import json
"""
前端頁面

請先在templates資料夾中建立HTML
然後依照以下方式建立一個連接到頁面的view:

def 頁面名稱(request):
    return render(request, '頁面名稱/index.html')

之後到 urls.py 來將網址聯繫到這個view
"""
def index(request):
    return render(request, 'index/index.html')

def home(request):
    return render(request, 'home/index.html')

def home2(request):
    return render(request, 'home2/index.html')

def login(request):
    return render(request, 'login/index.html')

def register(request):
    return render(request, 'register/index.html')

def logout(request):
    return render(request, 'logout/index.html')

def withdraw(request):
    return render(request, 'withdraw/index.html')

def pay_qr_code_page(request):
    return render(request, 'pay_qr_code_page/index.html')

def pay(request):
    return render(request, 'pay/index.html')

def deposit_upload(request):
    return render(request, 'deposit_upload/index.html')

def redeem_voucher_page(request):
    return render(request, 'redeem_voucher/index.html')
"""
API

使用方法如下:

def 此API的名稱(request):
    自己建立的model實例 = 自己建立的model()
    回傳結果 = 自己建立的model實例.方法(request)
    return HttpResponse(回傳結果)

之後到 urls.py 來將網址聯繫到這個view
"""
def api_login(request):
    login =Login()
    return login.login(request)

def api_logout(request):
    login =Login()
    return login.logout(request)

# 檢查登入 API
def api_check_login(request):
    login =Login()
    return login.check_login(request)

def api_register(request):
    register =Register()
    return register.register(request)

# 取得使用者帳號
def api_get_account(request):
    user = User()
    return user.get_account(request)

# 取得使用者Token
def api_get_token(request):
    toekn = ResolveRequest.ResolveToken(request)
    return HttpResponse(json.dumps({'code':1,'token':toekn}))
"""
密碼學 API
"""
def api_blind_signature_init(request):
    obj = PartiallyBlindSignature()
    return obj.init_blind_signature(request)

def api_blind_signature_get_Q(request):
    obj = PartiallyBlindSignaturePublicParameters()
    return obj.get_Q()

def api_blind_signature_get_K1(request):
    obj = PartiallyBlindSignaturePublicParameters()
    return obj.get_K1()

def api_blind_signature_get_q(request):
    obj =PartiallyBlindSignaturePublicParameters()
    return obj.get_q()

def api_blind_signature_step_1_get_K1_Q_bit_list(request):
    obj = PartiallyBlindSignature()
    return obj.api_blind_signature_step_1_get_K1_Q_bit_list(request)

def api_blind_signature_step_2_get_i_list(request):
    obj = PartiallyBlindSignature()
    return obj.api_blind_signature_step_2_get_i_list(request)

def api_blind_signature_step_5_get_C(request):
    obj = PartiallyBlindSignature()
    return obj.api_blind_signature_step_5_get_C(request)
"""
管理員登入登出
"""
def api_administrator_login(request):
    obj = AdministratorLogin()
    return obj.login(request)

def api_administrator_logout(request):
    login =AdministratorLogin()
    return login.logout(request)

# 檢查登入 API
def api_administrator_check_login(request):
    login =AdministratorLogin()
    return login.check_login(request)

"""
生成代金券
"""
# 生成代金券
def api_generate_voucher(request):
    obj = Voucher()
    return obj.generate_voucher(request)

# 兌換代金券
def redeem_voucher(request):
    obj = Voucher()
    return obj.redeem_voucher(request)

# 列出代金券
def list_voucher(request):
    obj = Voucher()
    return obj.list_voucher(request)
"""
使用者存款服務
"""
#以盲簽章兌換使用者存款
def redeem_currency(request):
    obj = RedeemCurrency()
    return obj.redeem_currency(request)
# 使用者查詢餘額
def get_balance(request):
    obj = GetBalance()
    return obj.get_balance(request)
# 取得使用者支付ID
def bank_user_payment_id(request):
    obj = GetUserPaymentID()
    return obj.get_user_payment_ID(request)
# 測試用提款接口
def withdraw_test(request):
    obj = WithdrawProxy()
    return obj.withdraw_proxy(request)
"""
使用者 AES 電子錢包
"""
# 設置電子錢包認證密文
def api_set_aes_verify_ciphertext(request):
    obj = AesVerifyKey()
    return obj.set_aes_verify_ciphertext(request)
# 取得電子錢包認證密文
def api_get_aes_verify_ciphertext(request):
    obj = AesVerifyKey()
    return obj.get_aes_verify_ciphertext(request)
"""
管理員登入頁面
"""
# 管理員登入
def administrator_login(request):
    return render(request, 'administrator_login/index.html')
# 管理員首頁
def administrator_home(request):
    return render(request, 'administrator_home/index.html')
# 管理員發行點數頁面
def  administrator_issue_voucher(request):
    return render(request, 'administrator_issue_voucher/index.html')
# 管理員交易紀錄檢視
def administrator_transaction_log(request):
    return render(request, 'administrator_transaction_log/index.html')

"""
管理取得紀錄
"""
# 管理員取得交易紀錄
def api_administrator_get_transaction_log(request):
    obj = TransactionLog()
    return obj.transaction_log(request)