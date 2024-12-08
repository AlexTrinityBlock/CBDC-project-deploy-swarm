import hashlib
import pprint
import json
import os
import redis
import ellipticcurve
from ellipticcurve.privateKey import PrivateKey, PublicKey
import gmpy2
import random
from app_core.services.YiModifiedPaillierEncryptionPy import YiModifiedPaillierEncryptionPy
"""
Note
=================
signer寄送-1

K1x: int，ECDSA 公鑰
K1y: int，ECDSA 公鑰
Qx: int，ECDSA 公鑰2
Qy: int，ECDSA 公鑰2
b_list: 一串0/1，20個。
=================
user寄送-2

C1: int:加密的訊息。
C2: int:加密的ECDSA鑰匙簽章。

ZeroKnowledgeProofC1List: List，20個C1'的零知識證明參數與(x,r')或者(x',r'')兩種混合成的序列。
ZeroKnowledgeProofC2List: List，20個C2'的零知識證明參數(x,r')或者(x',r'')兩種混合成的序列。

N: Yi的公鑰1
g: Yi的公鑰2

F1 ~ Fn: 加密的公開訊息Hash
=================
signer寄送-3

i_list: 20個，1~40之間的數字。
=================
user寄送-4

L: List，被選擇的l list，除了l_j
=================
signer寄送-5

C: int，簽章。
=================
"""
class PartiallyBlindSignatureServerInterface:
    def __init__(self, token:str):
        # 逾期時間(秒)
        self.expiretime = 1800
        # 從環境變數取得ECDSA鑰匙
        self.ECDSA_PUBLICKEY = os.environ['ECDSA_PUBLICKEY']
        self.ECDSA_PRIVATEKEY = os.environ['ECDSA_PRIVATEKEY']
        self.ECDSA_PUBLICKEY_2 = os.environ['ECDSA_PUBLICKEY_2']
        self.ECDSA_PRIVATEKEY_2 = os.environ['ECDSA_PRIVATEKEY_2']
        # 從ECDSA PUBLICKEY取得X,Y軸
        self.k1 = PrivateKey.fromPem(self.ECDSA_PRIVATEKEY).secret
        self.K1 = PublicKey.fromPem(self.ECDSA_PUBLICKEY)
        self.K1x = self.K1.point.x
        self.K1y = self.K1.point.y
        self.q = self.K1.curve.N
        # 第二把ECDSA 鑰匙對
        self.d = PrivateKey.fromPem(self.ECDSA_PRIVATEKEY_2).secret
        self.Q = PublicKey.fromPem(self.ECDSA_PUBLICKEY_2)
        self.Qx = self.Q.point.x
        self.Qy = self.Q.point.y
        # 公共參數
        self.G = PrivateKey.fromPem(self.ECDSA_PRIVATEKEY_2).curve.G
        self.curve_N = PrivateKey.fromPem(self.ECDSA_PRIVATEKEY_2).curve.N
        self.curve_A =PrivateKey.fromPem(self.ECDSA_PRIVATEKEY_2).curve.A
        self.curve_P = PrivateKey.fromPem(self.ECDSA_PRIVATEKEY_2).curve.P
        # 零知識證明次數
        self.NumberOfZeroKnowledgeProofRound = 20
        # User端的L長度
        self.LengthOfL = 40
        # User端的i長度
        self.LengthOfi = 20
        # User端的u長度
        self.LengthOfu = 10
        # Redis 連線
        self.redis_connection = redis.Redis(host=os.environ['REDIS_IP'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        # 檢查使用者當前進行到的步驟
        self.status = dict()
        self.create_or_load_status(token)
        #  F1~Fn
        self.F_list = None
        # i list
        self.i_list = None
        # 盲簽章
        self.C = None

    # 生成隨機二進位序列
    def generate_b_list(self):
        b_list = [ random.randrange(2) for i in range(self.NumberOfZeroKnowledgeProofRound) ]
        return b_list

    # 生成I
    def generate_I(self,text:str):
        h = hashlib.new('sha256')
        h.update(bytes(text, 'utf-8'))
        hex_string = h.hexdigest()
        message_hash = int(hex_string, 16)
        self.status["I"] = message_hash
        self.status["PublicInfomation"] = text

    # 零知識證明驗證
    def zero_knowledge_proof_vefify(self, input:dict):
        result = True
        Yi = YiModifiedPaillierEncryptionPy()
        # 零知識證明，重複驗證40次
        for i in range(self.NumberOfZeroKnowledgeProofRound):
            b = self.status["b_list"][i]
            ZeroKnowledgeProofC1List = input["ZeroKnowledgeProofC1List"]
            ZeroKnowledgeProofC2List = input["ZeroKnowledgeProofC2List"]
            C1p = ZeroKnowledgeProofC1List[i]['Cp']
            C2p = ZeroKnowledgeProofC2List[i]['Cp']
            # 若該次的詢問內容為0 
            if b == 0:
                C1_x = ZeroKnowledgeProofC1List[i]['x']
                C1_rp = ZeroKnowledgeProofC1List[i]['rp']
                C1p_test = Yi.encrypt(C1_x, self.status["N"], self.status["g"],C1_rp,self.q)

                C2_x = ZeroKnowledgeProofC2List[i]['x']
                C2_rp = ZeroKnowledgeProofC2List[i]['rp']
                C2p_test = Yi.encrypt(C2_x, self.status["N"], self.status["g"],C2_rp,self.q)

                if C1p_test != C1p:
                    result = False
                    break

                if C2p_test != C2p:
                    result = False
                    break
            # 若該次的詢問內容為1
            elif b == 1:
                C1_xp = ZeroKnowledgeProofC1List[i]['xp']
                C1_rpp = ZeroKnowledgeProofC1List[i]['rpp']
                C1C1p_mod_q = gmpy2.mod(gmpy2.mul(self.status['C1'], C1p), pow(self.status['N'],2))
                C1C1p_test = Yi.encrypt(C1_xp, self.status["N"],self.status["g"],C1_rpp,self.q)
                
                C2_xp = ZeroKnowledgeProofC2List[i]['xp']
                C2_rpp = ZeroKnowledgeProofC2List[i]['rpp']
                C2C2p_mod_q = gmpy2.mod(gmpy2.mul(self.status['C2'], C2p), pow(self.status['N'],2))
                C2C2p_test = Yi.encrypt(C2_xp, self.status["N"],self.status["g"],C2_rpp,self.q)

                if C1C1p_mod_q != C1C1p_test:
                    result = False
                    break
            
                if C2C2p_mod_q != C2C2p_test:
                    result = False
                    break
        return result

    # 生成 i list
    def generate_i_list(self):
        i_list = []
        for i in range(self.LengthOfu):
            u = random.randrange(self.LengthOfi)
            while u in i_list:
                u = random.randrange(self.LengthOfi)
            i_list.append(u)
        i_list.sort()
        self.i_list = i_list
        self.status["i_list"] = i_list

    # 驗證 F 與 l 之間的關聯
    def verify_L_F(self):
        Yi = YiModifiedPaillierEncryptionPy()
        F_list = self.status["F_list"].copy()
        L_list = self.status["L_list"].copy()
        i_list = self.status["i_list"].copy()
        j = self.status["j"]        
        F_p = set()
        F = set(F_list)        
        for i in range(len(L_list)):
            L_i_mul_I_mod_q = gmpy2.mod(L_list[i]*self.status['I'],self.q)
            Fi_p = Yi.encrypt(L_i_mul_I_mod_q,self.status['N'],self.status['g'],L_list[i],self.status['N'])
            F_p.add(Fi_p)
        if len(F_p & F) is not len(F_list)-1:
            raise Exception("F 驗證失敗",len(F - F_p ))

    # 建立盲簽章C
    def generate_C(self):
        Yi = YiModifiedPaillierEncryptionPy() # Yi的加解密
        r = Yi.generate_r(self.status["N"])  # 生成混淆r
        N_pow_2 = pow(self.status["N"], 2) 
        k1_mod_q_mod_inverse= gmpy2.invert(self.k1, self.q)
        self.k1_mod_q_mod_inverse = k1_mod_q_mod_inverse
        C1 = gmpy2.mpz(self.status["C1"])
        C2 = gmpy2.mpz(self.status["C2"])
        F1_to_Fn = self.status["F_list"]
        d = gmpy2.mpz(self.d)
        # 把C2^d 改成 C2^d mod q 
        C2_pow_d_mod_N_pow_2 = gmpy2.powmod(C2,self.d,pow(self.status["N"], 2)) # 無法肯定是否可行
        C1_C2_F_list_mul = C1*C2_pow_d_mod_N_pow_2
        self.C2_pow_d_mod_N_pow_2 = C2_pow_d_mod_N_pow_2
        # print("簽署者i list:",self.i_list)
        for i in self.status["i_list"]:
            Fi = self.status["F_list"][i]
            C1_C2_F_list_mul *= Fi
        temp1 = gmpy2.powmod(C1_C2_F_list_mul, k1_mod_q_mod_inverse, N_pow_2)
        result = gmpy2.mod(temp1 * gmpy2.powmod(r,self.status["N"],N_pow_2),N_pow_2)
        self.status["C"] = int(result)
        self.C = int(result)

    # 取得使用者輸入
    def input(self,input):
        input = json.loads(input)
        if self.status["step"] == 1:
            raise Exception("第一步驟，從簽署者輸出公鑰，不需要輸入任何東西。")
        elif self.status["step"] == 2:            
            self.status["C1"] = input["C1"]
            self.status["C2"] = input["C2"]
            self.status["N"] = input["N"]
            self.status["g"] = input["g"]
            self.status["F_list"] = input["F_list"]
            self.zero_knowledge_proof_vefify(input)
        elif self.status["step"] == 3:
            raise Exception('[盲簽章流程]', '錯誤的步驟')
        elif self.status["step"] == 4:
            self.status["L_list"] = input["L_list"]
            self.status["j"] = input["j"]
            self.verify_L_F()

    # 取得輸出
    def output(self):
        if self.status["step"] == 1:
            # 第一階段，簽署者將ECDSA公鑰K1與Q發佈，並且發佈零知識證明的提問b_list。
            return json.dumps({
                "K1x":self.K1x,
                "K1y":self.K1y,
                "b_list":self.status["b_list"],
                "Qx":self.Qx,
                "Qy":self.Qy,
                'I':self.status["I"],
                "PublicInfomation":self.status["PublicInfomation"]
            })
        if self.status["step"] == 2:
            raise Exception('[盲簽章流程]', '錯誤的步驟')
        if self.status["step"] == 3:
            # 從20個F中挑選任意10個，以0~19之間數值表示選擇的數字。
            self.generate_i_list()
            return json.dumps({"i_list":self.status["i_list"]})
        if self.status["step"] == 4:
            raise Exception('[盲簽章流程]', '錯誤的步驟')
        if self.status["step"] == 5:
            # 生成盲簽章C
            self.generate_C()
            return json.dumps({"C":self.C})

    # 儲存並且前進到下個步驟
    def save_and_next_step(self,token):
        status = json.loads(self.redis_connection.get(token))
        self.status['step'] += 1
        status['BlindSignature'] =  self.status
        self.redis_connection.set(token,json.dumps(status))
        self.redis_connection.expire(token, self.expiretime)

    # 創建新的認證狀態，或者載入舊的
    def create_or_load_status(self,token):
        status = json.loads(self.redis_connection.get(token))
        if 'BlindSignature' in status:
            self.status = status['BlindSignature']
        else:
            signature_status = dict()
            signature_status['step'] = 1
            signature_status['i_list'] = self.generate_i_list()
            signature_status['b_list'] = self.generate_b_list()
            status['BlindSignature'] =  signature_status
            self.redis_connection.set(token, json.dumps(status))
            self.redis_connection.expire(token, self.expiretime)
            self.status = status['BlindSignature']