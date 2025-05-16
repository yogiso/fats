from tqsdk import TqApi, TqAuth, TqAccount

# 1. 天勤免费数据账号
auth = TqAuth("yogiso", "630008260q")

# 2. 宏源仿真交易账户（CTP）
account = TqAccount(
    broker_id="3070",
    account_id="33336705",
    password="955888",
    # 注意：交易前置端口应为 32205（图中显示的 101.230.79.235:32205）
    td_url="tcp://101.230.79.235:32205"
)

# 3. 初始化 API 并拉取账户信息
api = TqApi(auth=auth, account=account)

acct = api.get_account()
print("登录成功，资金余额：", acct.balance)

# 4. 关闭 API
api.close()
