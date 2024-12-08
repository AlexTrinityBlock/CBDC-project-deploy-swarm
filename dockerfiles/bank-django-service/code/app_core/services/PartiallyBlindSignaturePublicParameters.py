import json
import os
from django.http import HttpResponse
from ellipticcurve.privateKey import PublicKey

class PartiallyBlindSignaturePublicParameters:
    def __init__(self):
        self.ECDSA_PUBLICKEY = os.environ['ECDSA_PUBLICKEY']
        self.ECDSA_PRIVATEKEY = os.environ['ECDSA_PRIVATEKEY']
        self.ECDSA_PUBLICKEY_2 = os.environ['ECDSA_PUBLICKEY_2']
        self.ECDSA_PRIVATEKEY_2 = os.environ['ECDSA_PRIVATEKEY_2']
        self.K1 = PublicKey.fromPem(self.ECDSA_PUBLICKEY)
        self.K1x = self.K1.point.x
        self.K1y = self.K1.point.y
        self.Q = PublicKey.fromPem(self.ECDSA_PUBLICKEY_2)
        self.Qx = self.Q.point.x
        self.Qy = self.Q.point.y
        self.q = self.K1.curve.N
    def get_Q(self):
        result = {
            "Qx":self.Qx,
            "Qy":self.Qy
        }
        return HttpResponse(json.dumps(result))

    def get_K1(self):
        result = {
            "K1x":self.K1x,
            "K1y":self.K1y
        }
        return HttpResponse(json.dumps(result))

    def get_q(self):
        result = {
            "q":self.q
        }
        return HttpResponse(json.dumps(result))
