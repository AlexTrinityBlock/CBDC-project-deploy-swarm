from django.urls import path

from . import views

# 網址連接到View
urlpatterns = [
    # 網站頁面
    path('', views.index, name='index'),
    path('index_en',views.index_en, name='index_en'),
    path('home', views.home2, name='home'),
    path('home_en', views.home2_en, name='home_en'),
    path('login', views.login, name='login'),
    path('login_en', views.login_en, name='login_en'),
    path('logout', views.logout, name='logout'),
    path('logout_en', views.logout_en, name='logout_en'),
    path('register',views.register, name = 'register'),
    path('register_en',views.register_en, name = 'register_en'),
    path('withdraw',views.withdraw, name = 'withdraw'),
    path('withdraw_en',views.withdraw_en, name = 'withdraw_en'),
    path('pay/qr-code',views.pay_qr_code_page, name = 'pay_qr_code_page'),
    path('pay/qr-code_en',views.pay_qr_code_page_en, name = 'pay_qr_code_page_en'),
    path('pay',views.pay, name = 'pay'),
    path('pay_en',views.pay_en, name = 'pay_en'),
    path('deposit/upload',views.deposit_upload, name = 'deposit_upload'),    
    path('deposit/upload_en',views.deposit_upload_en, name = 'deposit_upload_en'),   
    path('redeem/voucher',views.redeem_voucher_page, name = 'redeem_voucher'),
    path('redeem/voucher_en',views.redeem_voucher_page_en, name = 'redeem_voucher_en'),

    # 使用者登入API
    path('api/login', views.api_login),
    path('api/check_login', views.api_check_login),
    path('api/logout', views.api_logout),
    path('api/register',views.api_register),
    path('api/get/account',views.api_get_account),
    path('api/get/token',views.api_get_token),

    # 密碼學 API
    path('api/blind-signature/init',views.api_blind_signature_init),
    path('api/blind-signature/get/Q',views.api_blind_signature_get_Q),
    path('api/blind-signature/get/K1',views.api_blind_signature_get_K1),
    path('api/blind-signature/get/q',views.api_blind_signature_get_q),
    path('api/blind-signature/step/1/get/K1/Q/bit-list',views.api_blind_signature_step_1_get_K1_Q_bit_list),
    path('api/blind-signature/step/2/get/i-list',views.api_blind_signature_step_2_get_i_list),
    path('api/blind-signature/step/5/get/C',views.api_blind_signature_step_5_get_C),

    # 管理員專用API
    path('api/administrator/login', views.api_administrator_login),
    path('api/administrator/check_login', views.api_administrator_check_login),
    path('api/administrator/logout', views.api_administrator_logout),
    path('api/administrator/get/transaction_log', views.api_administrator_get_transaction_log),

    
    # 生成代金券序號
    path('api/generate/voucher', views.api_generate_voucher),
    path('api/redeem/voucher', views.redeem_voucher),
    path('api/list/voucher', views.list_voucher),

    # 使用者兌換貨幣
    path('api/redeem/currency', views.redeem_currency),
    path('api/get/balance', views.get_balance),
    path('api/get/user_payment_id', views.bank_user_payment_id),
    path('api/withdraw/test', views.withdraw_test),

    # 使用者 AES　功能，設置 AES 認證密文
    path('api/set/aes-verify-ciphertext', views.api_set_aes_verify_ciphertext),
    path('api/get/aes-verify-ciphertext', views.api_get_aes_verify_ciphertext),

    # 管理員登入頁面
    path('administrator/login', views.administrator_login),
    path('administrator/home', views.administrator_home,),
    path('administrator/issue/voucher', views.administrator_issue_voucher,),
    path('administrator/transaction_log', views.administrator_transaction_log,),

    path('administrator/login_en', views.administrator_login_en),
    path('administrator/home_en', views.administrator_home_en),
    path('administrator/issue/voucher_en', views.administrator_issue_voucher_en),
    path('administrator/transaction_log_en', views.administrator_transaction_log_en),
]

# 把不需要登入就可以瀏覽的頁面加入這裡
none_login_pages = [
    # 頁面
    "",
    "index_en",
    "register",
    "register_en",
    "login",
    "login_en",
    "administrator/login",
    "administrator/login_en",
    "administrator/home",
    "administrator/home_en",
    "administrator/issue/voucher",
    "administrator/issue/voucher_en",
    # API
    "api/login",
    "api/check_login",
    "api/register",
    "api/blind-signature/get/Q",
    "api/blind-signature/get/K1",
    "api/blind-signature/get/q",
    "api/administrator/login",
    "api/administrator/check_login",
    "api/administrator/logout",
    "api/administrator/check_login",
    "api/administrator/logout",
    "api/redeem/currency",
]