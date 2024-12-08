# 啟動腳本
import subprocess
import time

def main():
    for i in range(20):
        # 嘗試進行資料庫操作，如果操作失敗則嘗試重新連線，因為MySQL的啟動時間較長，所以重試直到連上。
        try:
            subprocess.run(['flask','run','--host=0.0.0.0'], check = True)
            break
        except subprocess.CalledProcessError:
            print("使用者密碼學支持伺服器失敗重試...")
        # 等待2秒重試
        time.sleep(2)
    # 嘗試20次後接受失敗，調整資料庫配置或者Django程式。
    raise Exception("使用者密碼學支持伺服器啟動失敗")

if __name__ == '__main__':
    main()