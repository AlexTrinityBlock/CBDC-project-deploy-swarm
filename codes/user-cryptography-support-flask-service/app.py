from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from services import YiModifiedPaillierEncryptionPy
import unittest
import sys
from services.Withdraw import Withdraw
from services.VerifyCurrency import VerifyCurrency
import json

app = Flask(__name__)
CORS(app)

# 簽章與獲得數位貨幣 API
@app.route("/withdraw",methods=['POST'])
def withdraw():
  withdraw = Withdraw()
  result = withdraw.withdraw(request)
  return result

# 驗證數位貨幣 API
@app.route("/verify/currency",methods=['POST'])
def verify_currency():
  Info = request.form['Info']
  message = request.form['message']
  t = int(request.form['t'],16)
  s = int(request.form['s'],16)
  R = int(request.form['R'],16)
  verify_currency = VerifyCurrency()
  if verify_currency.verify_currency(t,s,R,message,Info):
    return json.dumps({'code':1,'message':'Valid signature'})
  else:
    return json.dumps({'code':0,'message':'Invalid signature'})
  

# Flask 命令行
@app.cli.command()
def test():
  """
  運作測試
  """
  tests = unittest.TestLoader().discover("tests")
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  if result.errors or result.failures:
      sys.exit(1)