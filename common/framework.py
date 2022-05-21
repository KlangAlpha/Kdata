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



class API():
    def __init__(self,host=hostname):
        self.host = host

    def get_stocklist(self):
        url = self.host + "/stocklists"
        return requests.get(url)

    def post_stocklist(self,json):
        url = self.host + "/stocklists"
        resp = requests.post(url,json=json)
        return resp
    
    def create_factor(self,factorname,freq,describe=""):
        url = self.host + "/factormanages"
        requests.post(url,params={"factorname":factorname,"describe":describe,"freq":freq})

    def post_factora(self,factorname,json):
        url = self.host + "/postfactors"
        
        return requests.post(url,params={'factorname':factorname},json=json)

    def post_factorb(self,facotname,json):
        url = self.host + "/postfactors"
        return requests.post(url,params={'factorname':factorname},json=json)

    def get_factor(self,factorname,date=endday):
        url = self.host + "/getfactors"
        return requests.get(url,params={'factorname':factorname,'date':date})




