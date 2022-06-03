from operator import truediv
from common.common import get_date
from common.framework import API
import requests
import pandas as pd

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
# ROE
#


data = kapi.get_factor('roe',date=end).json()

roe = pd.DataFrame(data)
roe = roe[['code', 'date', 'value']]
roe = roe.query('value > "0.15"')

for i in range(len(roe)):
    code  = roe.iloc[i].code
    value = roe.iloc[i].value
    date  = roe.iloc[i].date
    print(code,getname(code),value,date)


#
# tdxgn 
#

data = kapi.get_factor('tdxgn',date=end).json()

import polars as pl
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