# scripts/test_sim_ok.py
import time
from tqsdk import TqApi, TqSim, TqAuth, TqKq

api = TqApi(
    TqSim(),
    auth=TqAuth("yogiso", "630008260q")
)

quote = api.get_quote("KQ.m@SHFE.rb")  # 任取螺纹钢主连
api.wait_update()                      # 收第一包行情
print("🟢 本地模拟 + 行情通道 OK，最新价:", quote.last_price)
api.close()
