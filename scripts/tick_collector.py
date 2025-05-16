#!/usr/bin/env python3
# scripts/tick_collector.py
"""
使用天勤 TqSdk + 宏源 CTP 仿真拉取 Tick 数据 → CSV
通过 Monkey-patch 直接屏蔽本地 WebHelper 插件冲突，保证既能使用付费账号认证，又能走 CTP 仿真。
"""
import os
import pandas as pd
from dotenv import load_dotenv
# —— 导入 TqSdk 核心组件 ——
from tqsdk import TqApi, TqAuth
# —— Monkey-patch：完全替换 WebHelper 为 DummyHelper，避免任何插件逻辑 ——
try:
    import tqsdk.tqwebhelper as wh
    class DummyHelper:
        def __init__(self, api=None):
            pass
        def _run(self):
            pass
        def join(self, timeout=None):
            pass
        def stop(self):
            pass
    wh.TqWebHelper = DummyHelper
except ImportError:
    pass

# —— 1. 清理掉天勤 OpenAPI 环境变量，强制使用 CTP 仿真 ——

os.environ.pop("TQ_WEBSOCKET", None)
os.environ.pop("TQ_DATA_DIR", None)

# —— 2. 加载 .env 中的 CTP_* + 快期账号 ——
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
username = os.getenv("TQ_USERNAME", "").strip()
password = os.getenv("TQ_PASSWORD", "").strip()
if not username or not password:
    raise RuntimeError("请在 .env 中配置并检查 TQ_USERNAME 和 TQ_PASSWORD（仅限纯 ASCII，无空格）")

# —— 3. 通过 TqAuth 进行快期帐号认证，然后连 CTP ——
auth = TqAuth(username, password)
api = TqApi(auth=auth)

# —— 4. 采集配置 ——
symbol      = "DCE.i2505"
count       = 10000
output_file = f"tick_{symbol.replace('.', '_')}.csv"

print(f"开始采集 {symbol} 的 {count} 条 Tick …")
ticks     = api.get_tick_serial(symbol)
collected = []
while len(collected) < count:
    api.wait_update()
    tick = ticks[-1]
    if tick.get("last_price") is None:
        continue
    collected.append(tick)

# —— 5. 清理并写入 CSV ——
api.close()
pd.DataFrame(collected).to_csv(output_file, index=False)
print(f"采集完成，已写入 → {output_file}")
