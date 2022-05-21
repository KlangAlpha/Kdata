# 筹码峰集中度 因子
from common.framework import API
from common.common import * # offset
import os


filename_cm = os.path.expanduser("~/.klang_stock_cm.csv")
if not os.path.exists(filename_cm):
    print("未发现筹码峰数据")
else:
    cm = 1
    cmdict = {}
    cmlist = []
    cm_list = open(filename_cm).readlines()
    cm_list = cm_list[1+int(offset):] #删除第一行

    for i in cm_list:
        ilist = i.split(',')
        code = ilist[0].split('.')[1].lower() + '.' + ilist[0].split('.')[0]
        cmdict[code] = ilist[2]
        cmlist.append({"code":code,"value":ilist[2]})

api = API()

# 筹码峰是不定时更新的，所以设置 freq = 0
api.create_factor('SCR',0,"筹码峰集中度")
api.post_factora('SCR',cmlist)
print("提交完成")

# 获取筹码峰数据
# resp = api.get_factor("SCR")

