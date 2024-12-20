#pytdx

import pandas as pd
from common.framework import API 
from common.common import * 
import json,os
import requests
import baostock as bs

bs.login()

start_d = get_date(5)

session = ""

@with_timeout(5)
def get_bar(name,code):
    bdata = bs.query_history_k_data_plus(code,'date,open,high,low,close,volume,amount,turn,code', start_date=start_d,frequency='d',adjustflag="2")
    datas = bdata.get_data()
    datas = datas [datas['volume'] > '0']

    print(name,code,end=" ")
    if len(datas) < 1:
        return 
    print(len(datas),datas.iloc[-1].date)
    df = datas.to_json(orient='table')
    jsondatas = json.loads(df)['data']
    for d in jsondatas:
        d['name'] = name
        del d['index']
    #print(jsondatas)
    #print(datas.iloc[-1],liutonggu,d)
    try:
        resp = session.post(kapi.host+"/dayks/updates",json=jsondatas,timeout=2000)
    except:
        time.sleep(2)
        session.post(kapi.host+"/dayks/updates",json=jsondatas,timeout=2000)


if True:

    kapi = API()

    stocklist = kapi.get_stocklist().json()
    session = requests.Session()
    for stock in stocklist[:]:
        code ,name = stock['code'],stock['name']    
        try:
            get_bar(name,code)
        except TimeoutException:
            pass
