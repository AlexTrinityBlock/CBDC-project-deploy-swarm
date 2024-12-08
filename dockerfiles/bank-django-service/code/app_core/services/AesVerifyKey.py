from app_core.models.AESKeyVerify import AESKeyVerify
from app_core.services.ResolveRequest import ResolveRequest
from django.http import HttpResponse
import json

class AesVerifyKey:

    def set_aes_verify_ciphertext(self,request):
        """
        設置 AES 驗證密文。
        """
        data = ResolveRequest.ResolvePost(request)
        AES_key_verify_model = AESKeyVerify()
        user_id = ResolveRequest.ResolveUserID(request)

        # 檢查 API 金鑰匙驗證密文是否被設置
        number_of_object= AESKeyVerify.objects.filter(user_id=user_id).count()
        if number_of_object > 0:
            AESKeyVerify.objects.filter(user_id=user_id).delete()

        # 設置 API 驗證 AES 密文
        AES_key_verify_model.aes_key_verify_ciphertext = data['aes_key_verify_ciphertext']
        AES_key_verify_model.user_id = user_id
        AES_key_verify_model.save()

        return HttpResponse(json.dumps({
            "code":1,
            "hint":"Success set aes key verify ciphertext"
        }))

    def get_aes_verify_ciphertext(self,request):
        """
        取得 AES 驗證密文。
        """
        data = ResolveRequest.ResolvePost(request)
        AES_key_verify_model = AESKeyVerify()
        user_id = ResolveRequest.ResolveUserID(request)

        # 檢查 API 金鑰匙驗證密文是否被設置
        number_of_object= AESKeyVerify.objects.filter(user_id=user_id).count()
        if number_of_object == 0:
            return HttpResponse(json.dumps({
            "code":0,
            "hint":"AES key verify ciphertext not be set."
            }))

        aes_key_verify_ciphertext = AESKeyVerify.objects.filter(user_id=user_id)[0].aes_key_verify_ciphertext

        return HttpResponse(json.dumps({
            "code":1,
            "hint":"Success get aes key verify ciphertext",
            "aes_key_verify_ciphertext":aes_key_verify_ciphertext
        }))