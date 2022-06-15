import baostock as bs
import pandas as pd
import json
import time
import os
from common.common import *
from common.framework import API

# 登录系统
lg = bs.login()
# 显示登录返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 获取行业分类数据
rs = bs.query_stock_industry()

filename_cm = os.path.expanduser("~/.klang_stock_cm.csv")

stock_list = []


now = int(time.time())
now = now - 30 * 24 * 3600 #往前30天
timeArray = time.localtime(now)
start_date = time.strftime("%Y-%m-%d", timeArray)

while (rs.error_code == '0') & rs.next() :
    # 获取一条记录，将记录合并在一起
    row = rs.get_row_data()
    kdata = bs.query_history_k_data_plus(row[1], 'date,open,high,low,close,volume', start_date=start_date, 
                                      frequency='d')	
    
    if len(kdata.get_data()) <= 10:
        continue

    print(row)
    stock_list.append([row[1],row[2]]) # code,name	


datas = pd.DataFrame(stock_list, columns=['code','name'])

datas = datas.to_json(orient='table',index=False)
jsondatas = json.loads(datas)['data']

api = API()
print("提交到Klang 数据服务器")
resp = api.post_stocklist(jsondatas)
print(resp.content)

bs.logout()
