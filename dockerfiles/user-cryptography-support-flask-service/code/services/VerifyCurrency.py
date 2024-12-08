import hashlib
from operator import ge
from pprint import pprint
import json
import os
from unittest import result
import ellipticcurve
from ellipticcurve.privateKey import PrivateKey, PublicKey
import gmpy2
import random
from math import gcd
from copy import deepcopy
from .YiModifiedPaillierEncryptionPy import YiModifiedPaillierEncryptionPy
import requests

class VerifyCurrency:
    def __init__(self):
        #  URL
        self.url = os.environ['BANK_DJANGO_SERVICE_URL']
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
        self.Q = json.loads(requests.get(self.url+'/api/blind-signature/get/Q').text)
        self.Qx = self.Q['Qx'] # 簽署者 ECDSA 的公鑰x座標
        self.Qy = self.Q['Qy'] # 簽署者 ECDSA 的公鑰y座標

    def hash(self, message:str):
        """Hash函數H()

        使用SHA256，Hash算法
        """
        h = hashlib.new('sha256')
        h.update(bytes(message, 'utf-8'))
        hex_string = h.hexdigest()
        message_hash = int(hex_string, 16)
        return message_hash

    def verify_currency(self, t:int ,s:int, R:int, message:str, public_message:str):
        self.s = s
        self.t = t
        self.message_hash = self.hash(message)
        self.I = self.hash(public_message)
        self.R = int(gmpy2.mod(R,self.q))
        s_mod_q_inverse = gmpy2.invert(self.s, self.q)

        u = int(gmpy2.mod(s_mod_q_inverse*(self.message_hash+(self.R * self.I)), self.q))
        v = int(gmpy2.mod(s_mod_q_inverse * self.t, self.q))

        G = ellipticcurve.point.Point(self.curve_Gx, self.curve_Gy)
        Q = ellipticcurve.point.Point(self.Qx, self.Qy)

        uG = ellipticcurve.math.Math.multiply(G, u, self.curve_N, self.curve_A, self.curve_P)
        vQ = ellipticcurve.math.Math.multiply(Q, v, self.curve_N, self.curve_A, self.curve_P)

        K_p = ellipticcurve.math.Math.add(uG, vQ, self.curve_A, self.curve_P)
        t_p = gmpy2.mod(K_p.x,self.q)

        if self.t == t_p:
            return True
        else:
            return False