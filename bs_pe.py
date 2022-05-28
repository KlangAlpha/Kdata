#
# baostock
#
# PE:市盈率 = 股价 / 每股盈利=总市值 /净利润

from common.common import * # get_date
from common.framework import API
import baostock as bs

kapi = API() #klang data api
stocklist = kapi.get_stocklist().json()

#create_factor 创建B类因子,1 是B类因子
kapi.create_factor('pe',1,"动态日更PE")

# 登录系统
bs.login()

def get_pe(code):
    result = []
    # "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",

    rs = bs.query_history_k_data_plus(code,
    "date,code,peTTM",
    start_date='2020-01-01', end_date=get_date(0), 
    frequency="d", adjustflag="3")

    data = rs.get_data()
    # print(data)
    for index in range(len(data)):
        result.append({
            "pe": data.iloc[index]['peTTM'],
            "date":data.iloc[index]['date'],
            "code":code})

    kapi.post_factorb('pe',result);   

for stock in stocklist:
    code ,name = stock['code'],stock['name']
    print(code,name) 
    get_pe(code)
