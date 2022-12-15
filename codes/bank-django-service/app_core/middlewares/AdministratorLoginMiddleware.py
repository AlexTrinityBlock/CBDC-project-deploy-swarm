from django.shortcuts import redirect
from app_core.services.ResolveRequest import ResolveRequest
from app_core.urls import none_login_pages

class AdministratorLoginMiddleware:
    """
    管理員登入驗證中間層
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # 登錄要登入的頁面
        self.admin_login_require_page = [
            'administrator/home',
            'administrator/issue/voucher',
            'administrator/transaction_log'
        ]
    
    def check_path_in_list(self,path:str):
        """
        檢查路徑是否在管理員需要登入頁面中。
        """
        for path_in_list in self.admin_login_require_page:
            if path == ('/' + path_in_list):
                return True
        return False

    def check_path_in_user_list(self,path:str):
        """
        檢查路徑是否在一般使用者不需要登入頁面中。
        """
        for path_in_list in none_login_pages:
            if path == ('/' + path_in_list):
                return True
        return False

    def __call__(self, request):
        # 嘗試取得登入使用者角色
        try:
            role = ResolveRequest.ResolveRole(request)
        except:
            role = None

        # 若路徑在管理員需要登入頁面
        require_login = self.check_path_in_list(request.path)

        # 確認是否為管理員
        if require_login and (role != 'administrator'):
            return redirect("/administrator/login")

        # 若已經登入，從任何頁面轉跳到管理員首頁
        if (not require_login) and (role == 'administrator') and (not request.path.startswith("/api")) and (not request.path.startswith("/logout")):
            print(require_login)
            print(request.path)
            return redirect("/administrator/home")

        response = self.get_response(request)
        
        return response
