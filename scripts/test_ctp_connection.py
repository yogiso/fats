# test_ctp_connection.py
import os
from tqsdk import TqApi, TqAuth

# 从环境变量读取
user = os.getenv("TQ_USER")
pwd  = os.getenv("TQ_PASS")
if not user or not pwd:
    raise RuntimeError("请先在 ~/.bash_profile 设置 TQ_USER 和 TQ_PASS 并 source 生效")

# 建立 TqSdk 连接并打印账户信息
api = TqApi(auth=TqAuth(user, pwd))
account = api.get_account()
print("CTP 账户信息：", account)
api.close()
