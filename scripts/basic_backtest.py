#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from tqsdk import TqApi, TqAuth

def main():
    user = os.getenv("TQ_USER")
    pwd  = os.getenv("TQ_PASS")
    if not user or not pwd:
        raise RuntimeError("请设置 TQ_USER/TQ_PASS 并 source ~/.bash_profile")

    # —— 建立连接 ——
    api = TqApi(auth=TqAuth(user, pwd))
    try:
        symbol      = "DCE.i2505"
        interval_ms = 60 * 1000
        n_bars      = 10

        klines = api.get_kline_serial(symbol, interval_ms, data_length=n_bars)

        print(f"\n【历史数据】{symbol} — 共 {len(klines)} 根 1min K 线：\n")
        print(klines)

        csv_name = f"{symbol.replace('.', '_')}_{interval_ms//1000}s_{len(klines)}.csv"
        klines.to_csv(csv_name, index=False)
        print(f"\nCSV 已保存 → {csv_name}\n")

        # （可选）实时监听新 Bar
        # while api.wait_update():
        #     if api.is_changing(klines.iloc[-1], ["datetime"]):
        #         print("【新 Bar】", klines.iloc[-1])

    finally:
        api.close()

if __name__ == "__main__":
    main()
