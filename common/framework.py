from .common import * #hostname
import numpy as np
import pandas as pd
import requests

# print 打印color 表
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKRED = '\033[31m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

session = requests.Session()

class API():
    def __init__(self,host=hostname,hostget=hostnameget):
        self.host = host
        self.hostget = hostget

    def get_stocklist(self):
        url = self.hostget + "/stocklists"
        return session.get(url)

    def post_stocklist(self,json):
        url = self.host + "/stocklists"
        resp = session.post(url,json=json)
        return resp
    
    def create_factor(self,factorname,freq,describe=""):
        url = self.host + "/factormanages"
        session.post(url,params={"factorname":factorname,"describe":describe,"freq":freq})

    def post_factora(self,factorname,json,date=None):
        url = self.host + "/postfactors"
        if date is None:
            return session.post(url,params={'factorname':factorname},json=json)
        else:
            return session.post(url,params={'factorname':factorname,"date":date},json=json)

    def post_factorb(self,factorname,json):
        url = self.host + "/postfactors"
        return session.post(url,params={'factorname':factorname},json=json)

    def get_factor(self,factorname,date=endday,code='sh.600000',limit=100):
        url = self.hostget + "/getfactors"
        return session.get(url,params={'factorname':factorname,
            "code":code,
            "limit":limit,
            'date':date})

    def create_group(self,name,description):
        url = self.host + "/groupmanagers"
        return session.post(url,params={"name":name,"description":description})

    #为了解决参数顺序问题，设置了默认参数None，但是设置None是不允许的。
    def add_togroup(self,name=None,code=None,date=None,vol=None):
        if name is None or code is None or date is None or vol is None:
            return "need more params"

        url = self.host + "/grouplists"
        return session.post(url,params={"name":name,
            "code":code,
            "vol":vol,
            "status":1,
            "date":date})

    
    def del_fromgroup(self,name=None,code=None,date=None,vol=None):
        if name is None or code is None or date is None or vol is None:
            return "need more params"

        url = self.host + "/grouplists"
        return session.post(url,params={"name":name,
            "code":code,
            "vol":vol,
            "status":-1,
            "date":date})

    def codes_fromgroup(self,name,start,end):
        url = self.hostget + "/grouplists"
        resp = session.get(url,params={"name":name,"start":start,"end":end})
        if resp.status_code != 200:
            return resp

        # 去掉重复语句
        codelist = []
        result = []
        for i in resp.json():
            if i['code'] not in codelist:
                result.append(i)
            codelist.append(i['code'])
        return result
    def create_strategy(self,title,content,description,status,lang):
        url = self.host + "/strategies"
        return session.post(url,json={"title":title,
            'content':content,
            'description':description,
            'status':status,
            'lang':lang})

    def get_strategy(self,params):
        url = self.hostget + "/strategies"
        return session.get(url,params)


