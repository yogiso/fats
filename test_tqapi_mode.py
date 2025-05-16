#!/usr/bin/env python3
# test_tqapi_mode.py

import os
from tqsdk import TqApi, TqAuth
from dotenv import load_dotenv

# 1. 加载 .env
load_dotenv()

symbol = "SHFE.rb2310"  # 测试合约，可改

# —— 模式 A: 免费远程行情 —— 
print("模式 A：免费行情（不传 auth）")
try:
    api_free = TqApi()
    quote_free = api_free.get_quote(symbol)
    # 只打印能说明行情正常返回的字段
    print(f"  免费 last_price = {quote_free.last_price}  时间 = {quote_free.datetime}")
    api_free.close()
except Exception as e:
    print(f"  模式 A 报错：{e}")

print("\n" + "-"*50 + "\n")

# —— 模式 B: 带凭据登录 —— 
user = os.getenv("TQ_USERNAME", "").strip()
pwd  = os.getenv("TQ_PASSWORD", "").strip()
if not (user and pwd):
    print("模式 B：未检测到 TQ_USERNAME/TQ_PASSWORD，跳过带 auth 模式")
else:
    print("模式 B：登录行情（传入 auth）")
    try:
        api_auth = TqApi(auth=TqAuth(user, pwd))
        quote_auth = api_auth.get_quote(symbol)
        print(f"  认证 last_price = {quote_auth.last_price}  时间 = {quote_auth.datetime}")
        api_auth.close()
    except Exception as e:
        print(f"  模式 B 报错：{e}")
