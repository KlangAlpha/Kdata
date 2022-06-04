
from common.common import get_date
from common.framework import API
import requests
import pandas as pd
import polars as pl

end = get_date(0)
kapi = API() #klang data api

stocklist = kapi.get_stocklist().json()
stockindex = {}


#
#  初始化股票列表
#

i = 0 
for stock in stocklist:
    stockindex[stock['code']] = i
    i += 1

def getname(code):
    return stocklist[stockindex[code]]['name']

#
# ROE  A类因子，适合产生股票列表
#


data = kapi.get_factor('roe',date=end).json()

roe = pl.DataFrame(data)

roe = roe.select([
    'code',
    'value',
    'date'
])

roe = roe.filter(pl.col('value') > "0.15")
    
roe = roe.with_columns([
    pl.col("code").apply(lambda s: getname(s)).alias('name')
])

print(roe)


#
# tdxgn A类因子适合产生股票列表
#

data = kapi.get_factor('tdxgn',date=end).json()


df1 = pl.DataFrame(data)
df1 = df1.select([
    'factorname',
    'code',
    'value',
    'date'
])

def contains(s,key):  
    if key in s:
        return True
    else:
        return False
    
df1 = df1.filter(
    pl.col("value").apply(lambda s: contains(s,"光伏"))
)

print(df1)


#
# MACD B类因子，适合产生数据和算法加工
#
#

stock =  stocklist[100]
code = stock['code']

data = kapi.get_factor('macd',date=end,code=code,limit=200).json()

df_macd = pl.DataFrame(data)

def buy(s):
    result = s.split(",")
    if len(result) == 5:
        return int(result[3])
    else:
        return 0
def sell(s):
    result = s.split(",")
    if len(result) == 5:
        return int(result[4])
    else:
        return 0

df_macd = df_macd.with_columns([
    pl.col("macd").apply(lambda s: buy(s)).alias('buy'),
    pl.col("macd").apply(lambda s: sell(s)).alias('sell')
])


df_b = df_macd.filter(
    pl.col("buy") == 1
)
df_s = df_macd.filter(
    pl.col("sell") == 1
)
print(df_b)
print(df_s)


def buy_condition(dt):
    return df_macd[df_macd['date'] == dt].buy[0] == 1
    

def sell_condition(dt):
    return df_macd[df_macd['date'] == dt].sell[0]  == 1
    

import btr
from Klang import Kl,Klang
Klang.Klang_init(); #加载所有股票列表
     
Kl.code("sh.600126")
df = Kl.currentdf['df'] 

btr.set_buy_sell(buy_condition,sell_condition)
btr.init_btr(df)

