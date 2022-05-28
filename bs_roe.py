#
# baostock
#
# PE:市盈率 = 股价 / 每股盈利=总市值 /净利润

from common.common import * # get_date
from common.framework import API
import baostock as bs

kapi = API() #klang data api
stocklist = kapi.get_stocklist().json()

#create_factor 创建A类因子,0是A类因子,1 是B类因子
kapi.create_factor('ROE',0,"季度ROE AVG,数据来自baostock")

# 登录系统
bs.login()
result = []
date = ""
def get_roe(code):
    global date 
    rs = bs.query_profit_data(code=code, year=2022, quarter=1)

    data = rs.get_data()
    #data.iloc[0]['statDate'],data.iloc[0]['roeAvg']
    if len(data) == 0:
        return 
    result.append({
        'code':code,
        'value':data.iloc[0]['roeAvg'],
    })
    date = data.iloc[0]['statDate']

for stock in stocklist:
    code ,name = stock['code'],stock['name']
    print(code,name) 
    get_roe(code)

kapi.post_factora('roe',result,date = date);  