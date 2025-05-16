#!/usr/bin/env python3
import os, time
from dotenv import load_dotenv
from tqsdk import TqApi, TqAuth, TqAccount

# 1. 加载 .env
load_dotenv()
# 免费版登录凭据（天勤账户, 用于鉴权）
user   = os.getenv("TQ_USERNAME", "").strip()
pwd    = os.getenv("TQ_PASSWORD", "").strip()
# CTP 仿真通道参数
broker = os.getenv("CTP_BROKER_ID", "").strip()
investor = os.getenv("CTP_INVESTOR_ID", "").strip()
ctp_pwd  = os.getenv("CTP_PASSWORD", "").strip()
md_url   = os.getenv("CTP_MD_FRONT", None)
td_url   = os.getenv("CTP_TD_FRONT", None)

# 2. 建立 CTP 仿真行情连接
ctp_acc = TqAccount(broker, investor, ctp_pwd, md_url, td_url)
api     = TqApi(ctp_acc, auth=TqAuth(user, pwd))

# 3. 订阅你关心的期货合约
symbol = "SHFE.rb2310"
quote  = api.get_quote(symbol)

print(f"开始抓取 CTP 仿真频道的 {symbol} 实时行情……(Ctrl+C 停止)\n")

# 4. 持续打印盘口和最新成交
try:
    while True:
        api.wait_update()  # 等待任何数据更新
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
