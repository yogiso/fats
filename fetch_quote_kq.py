#!/usr/bin/env python3
# fetch_quote_kq.py — 使用快期模拟通道 (TqKq) 持续抓取期货行情

import os
import time
from dotenv import load_dotenv
from tqsdk import TqApi, TqAuth, TqKq

# 1. 加载 .env（确保已配置 TQ_USERNAME 和 TQ_PASSWORD）
load_dotenv()
user = os.getenv("TQ_USERNAME", "").strip()
pwd  = os.getenv("TQ_PASSWORD", "").strip()

if not (user and pwd):
    raise RuntimeError("请在 .env 中配置 TQ_USERNAME 和 TQ_PASSWORD，用于快期模拟登录。")

# 2. 建立快期模拟通道
api = TqApi(TqKq(), auth=TqAuth(user, pwd))

# 3. 订阅期货合约（示例：螺纹钢 2310 合约）
symbol = "SHFE.rb2310"
quote = api.get_quote(symbol)

print(f"开始使用快期模拟通道抓取 {symbol} 实时行情（按 Ctrl+C 停止）…\n")

# 4. 持续循环输出最新盘口和成交价
try:
    while True:
        api.wait_update()  # 等待任何行情更新
        print(
            f"{quote.datetime} | "
            f"last_price={quote.last_price} | "
            f"bid1={quote.bid_price1}({quote.bid_volume1}) | "
            f"ask1={quote.ask_price1}({quote.ask_volume1})"
        )
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n已停止抓取。")
finally:
    api.close()
