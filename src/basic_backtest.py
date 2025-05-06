# src/basic_backtest.py

import requests
import backtrader as bt
import datetime
import pandas as pd

# —— 1. 获取历史行情 —— 
def fetch_ohlcv(symbol='BTCUSDT', timeframe='1h', limit=100):
    """
    直接调用 Binance /klines 接口，避免加载 exchangeInfo 导致超时。
    """
    url = (
        'https://api.binance.com/api/v3/klines'
        f'?symbol={symbol}&interval={timeframe}&limit={limit}'
    )
    resp = requests.get(url, timeout=120)    # 最长等 120 秒
    resp.raise_for_status()
    data = resp.json()
    return [
        (
            datetime.datetime.fromtimestamp(d[0] / 1000),
            float(d[1]), float(d[2]), float(d[3]),
            float(d[4]), float(d[5])
        )
        for d in data
    ]

# —— 2. 定义最简策略 —— 
class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                self.buy(size=0.001)
        else:
            if self.dataclose[0] > self.dataclose[-1]:
                self.close()

# —— 3. 运行回测 —— 
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # 1. 拉取原始 K 线数据
    raw = fetch_ohlcv()

    # 2. 转成 Pandas DataFrame，并设置时间索引
    df = pd.DataFrame(
        raw,
        columns=['datetime', 'open', 'high', 'low', 'close', 'volume']
    )
    df.set_index('datetime', inplace=True)

    # 3. 用 Backtrader 的 PandasData 载入数据
    data_feed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data_feed)

    # 4. 加入策略、设置初始资金并运行
    cerebro.addstrategy(TestStrategy)
    cerebro.broker.setcash(10000.0)

    print('Starting Portfolio Value:', cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value:', cerebro.broker.getvalue())
