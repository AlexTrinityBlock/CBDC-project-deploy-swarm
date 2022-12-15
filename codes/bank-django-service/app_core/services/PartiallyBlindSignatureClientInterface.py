import hashlib
from operator import ge
from pprint import pprint
import json
import os
from unittest import result
import redis
import ellipticcurve
from ellipticcurve.privateKey import PrivateKey, PublicKey
import gmpy2
import random
from math import gcd
from copy import deepcopy
from .YiModifiedPaillierEncryptionPy import YiModifiedPaillierEncryptionPy
"""
Note
=================
signer寄送-1

K1x: int，ECDSA 公鑰
K1y: int，ECDSA 公鑰
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
class PartiallyBlindSignatureClientInterface:
    def __init__(self):
        self.n = 40 # 決定隨機數l_list的數字數量
        
        # Yi的公私鑰匙
        # 私鑰
        self.p = None
        self.k = None
        # 公鑰
        self.N = None
        self.g = None

        # 二進位序列
        self.b_list = None

        # 訊息相關與Hash
        self.message_hash = None # 訊息的SHA256轉換成整數
        self.I = None # 雙方共識訊息info的hash

        # 加密混淆用隨機數
        self.r1 = None
        self.r2 = None

        # 私鑰
        self.k2 = None

        # 密文
        self.C1 = None
        self.C2 = None

        # ECDSA曲線參數 - secp256k1
        self.G = PublicKey.fromPem(os.environ['ECDSA_PUBLICKEY']).curve.G
        self.curve_Gx = self.G.x
        self.curve_Gy = self.G.y
        self.curve_A = PublicKey.fromPem(os.environ['ECDSA_PUBLICKEY']).curve.A
        self.curve_B = PublicKey.fromPem(os.environ['ECDSA_PUBLICKEY']).curve.B
        self.curve_N = PublicKey.fromPem(os.environ['ECDSA_PUBLICKEY']).curve.N
        self.curve_P = PublicKey.fromPem(os.environ['ECDSA_PUBLICKEY']).curve.P
        self.q = self.curve_N

        # ECDSA 點
        self.K = None # 使用者 ECDSA 的公鑰x,y座標，可以用 self.K.x, self.K.y
        self.K1 = None # 簽署者 ECDSA 的公鑰x,y座標，self.K1.x, self.K1.y
        self.Qx = None # 簽署者 ECDSA 的公鑰x座標
        self.Qy = None # 簽署者 ECDSA 的公鑰y座標

        # 零知識證明次數
        self.NumberOfZeroKnowledgeProofRound = 20

        # 列表
        self.l_list = None # 由n個小於phi(N^2)並且與N互質的整數組成。
        self.LengthOfL = 40 # L 列表長度
        self.F_list = None
        self.i_list = None

        # 盲簽章
        self.C = None 
        self.s = None
        self.t = None # 用來簽署簽署者的公鑰的數值
        self.R = None

    def set_K1(self, K1_x, K1_y):
        """設置點K1

        K1是個由 x, y 兩座標組成的橢圓曲線上的點，也就是簽署者 ECDSA 的公鑰。
        """
        self.K1 = ellipticcurve.point.Point(K1_x, K1_y) # 使用ECDSA函數庫的點物件

    def hash_H(self, message:str):
        """Hash函數H()

        使用SHA256，Hash算法
        """
        bytes_string = bytes(message, 'utf-8')
        h = hashlib.new('sha256')
        h.update(bytes(message, 'utf-8'))
        hex_string = h.hexdigest()
        message_hash = int(hex_string, 16)
        return message_hash

    def generate_message_hash(self, message:str):
        """設置訊息的Hash值

        輸入訊息後，自動生成Hash值
        """
        self.message_hash = self.hash_H(message) 
        return self.message_hash

    def generate_I(self, info:str):
        self.I = self.hash_H(info)
        return self.I

    def generate_r(self):
        N = self.N
        r = 0
        r = self.find_random_co_prime(pow(N,2))
        self.r = gmpy2.mpz(r)
        return r

    def generate_t(self):
        Kx = gmpy2.mpz(self.K.x)
        t = gmpy2.mod(Kx, self.q)
        return int(t)

    def find_random_co_prime(self, n:int):
        result = random.randrange(deepcopy(n)) #尋找極限以下的隨機數
        while gcd(n,result) != 1: # 當與n不互質時
            result += 1 # 往下個數值進行線性搜索。
            if result > n : # 若結果不小心大於目標
                result = random.randrange(deepcopy(n)) #重新尋找隨機數
        return result

    def generate_l_list(self):
        phi_N_square = pow(gmpy2.mul(gmpy2.mul(self.p-1, self.q-1), self.k-1), 2) # phi(N^2)，N平方的歐拉函數
        l_list = []
        for i in range(self.LengthOfL):
            l_list.append(self.find_random_co_prime(phi_N_square))
        return l_list

    def encrypt(self, m:int, N:int, g:int ,r:int, q:int):
        N, g, r, m= gmpy2.mpz(N), gmpy2.mpz(g), gmpy2.mpz(r), gmpy2.mpz(m)
        N_power_2 = pow(N,2)
        # 此處將算式改為 C = [(g^m mod N^2) * (r^N mod N^2)] mod N^2 ，防止數值過大導致的記憶體占滿，或者速度緩慢。
        C = gmpy2.mod(gmpy2.powmod(g, m, N_power_2) * gmpy2.powmod(r, N, N_power_2), N_power_2)
        return int(C)

    def step1_input(self, input:str):
        input_object = json.loads(input)
        self.set_K1(input_object["K1x"], input_object["K1y"])
        self.b_list = input_object["b_list"]
        self.Qx = input_object["Qx"]
        self.Qy = input_object["Qy"]

    def generate_zero_know_proof_parameter_set(self,info:int,r:int,b:int)->dict:
        """
        生成零知識證明參數
        如果是C1的話info 就是 Hash(m)
        如果是C2的話info就是Hash(info)
        """
        Yi = YiModifiedPaillierEncryptionPy()
        result = dict()
        temp = dict()
        temp['x'] = random.randrange(self.q)
        temp['rp'] = self.generate_r()
        temp['xp'] = gmpy2.mod(gmpy2.add(info, temp['x']), self.q)
        temp['rpp'] = self.rpp = gmpy2.mod(gmpy2.mul(r, temp['rp'] ), pow(self.N,2))

        if b == 0:
            result['x'] = int(temp['x'])
            result['rp'] = int(temp['rp'])
        elif b == 1:
            result['xp'] = int(temp['xp'])
            result['rpp'] = int(temp['rpp'])

        result['Cp'] = Yi.encrypt(temp['x'], self.N, self.g, temp['rp'], self.q)

        return result

    def generate_zero_know_proof_parameter_sets(self):
        """
        生成多組C1,C2的零知識證明參數
        """
        result = dict()

        C1_zero_know_proof_parameter_sets = []
        C2_zero_know_proof_parameter_sets = []

        for i in range(self.NumberOfZeroKnowledgeProofRound):
            b = self.b_list[i]
            C1_zero_know_proof_parameter_sets.append(self.generate_zero_know_proof_parameter_set(self.message_hash,self.r1,b))
            C2_zero_know_proof_parameter_sets.append(self.generate_zero_know_proof_parameter_set(self.t,self.r2,b))

        result['ZeroKnowledgeProofC1List'] = C1_zero_know_proof_parameter_sets
        result['ZeroKnowledgeProofC2List'] = C2_zero_know_proof_parameter_sets

        return result

    def generate_F_list(self):
        '''
        生成 F list
        '''
        Yi = YiModifiedPaillierEncryptionPy()
        F_list = []
        for i in range(self.LengthOfL):
            l_i_mul_I = gmpy2.mul(self.l_list[i], self.I)
            l_i_mul_I_mod_q = gmpy2.mod(l_i_mul_I, self.q)
            F_i = Yi.encrypt(l_i_mul_I_mod_q,self.N,self.g,self.l_list[i],self.q)
            F_list.append(F_i)
        return F_list 

    def generate_keypairs_parameters(self):
        # 生成Yi的公私鑰
        Yi = YiModifiedPaillierEncryptionPy()
        Yi.generate_keypairs(self.q)
        self.p = Yi.p 
        self.k = Yi.k
        self.N = Yi.N
        self.g = Yi.g
        self.r1 = self.generate_r()
        self.r2 = self.generate_r()
        self.k2 = self.find_random_co_prime(self.q)
        self.K = ellipticcurve.math.Math.multiply(self.K1, int(self.k2), self.curve_N, self.curve_A, self.curve_P)
        self.t = self.generate_t()
        self.C1 = self.encrypt(self.message_hash, self.N, self.g, self.r1, self.q)
        self.C2 = self.encrypt(self.t, self.N, self.g, self.r2, self.q)
        self.l_list = self.generate_l_list()
        self.F_list = self.generate_F_list()

    def step1_output(self):
        result = self.generate_zero_know_proof_parameter_sets()
        result['N'] = int(self.N)
        result['g'] = int(self.g)
        result['C1'] = int(self.C1)
        result['C2'] = int(self.C2)
        result['F_list'] = self.F_list
        return json.dumps(result)

    def step3_input(self, input:str):
        input_object = json.loads(input)
        self.i_list = input_object["i_list"]

    def step4_output(self):
        self.j = random.choice(self.i_list)
        l_list = self.l_list.copy()
        del l_list[self.j]
        result = dict()
        result['L_list'] = l_list
        result['j'] = self.j
        return json.dumps(result)

    def step5_input(self, input:str):
        Yi = YiModifiedPaillierEncryptionPy()
        input_object = json.loads(input)
        self.C = input_object["C"]
        temp1 = Yi.decrypt(self.C,self.p, self.k, self.q, self.N)
        self.temp1 = temp1
        k2_mod_q_inverse = gmpy2.invert(self.k2, self.q)
        self.s = int(gmpy2.mod(k2_mod_q_inverse*temp1, self.q))
        # print("使用者i list:",self.i_list)
        R = 0
        for i in self.i_list:
            R += self.l_list[i]
        self.R = int(gmpy2.mod(R,self.q))
        s_mod_q_inverse = gmpy2.invert(self.s, self.q)

        u = int(gmpy2.mod(s_mod_q_inverse*(self.message_hash+(self.R * self.I)), self.q))
        v = int(gmpy2.mod(s_mod_q_inverse * self.t, self.q))

        G = ellipticcurve.point.Point(self.curve_Gx, self.curve_Gy)
        Q = ellipticcurve.point.Point(self.Qx, self.Qy)

        uG = ellipticcurve.math.Math.multiply(G, u, self.curve_N, self.curve_A, self.curve_P)
        vQ = ellipticcurve.math.Math.multiply(Q, v, self.curve_N, self.curve_A, self.curve_P)

        K_p = ellipticcurve.math.Math.add(uG, vQ, self.curve_A, self.curve_P)
        self.t_p = gmpy2.mod(K_p.x,self.q)

        # print("t",self.t)
        # print("t'",K_p.x%self.q)
        # print("Kx'",K_p.x)
        # print("Kx",self.K.x)