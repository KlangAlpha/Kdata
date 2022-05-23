#
# Kdata 组接口
#
# 注意：⚠️ 组结算时按照提交的先后顺序即时结算的。如果提交时间错乱会导致无法计算。
#
from common.framework import API

kapi = API()

kapi.create_group("建筑","目前建筑板块正在启动")

code = "sz.003214" #测试数据
kapi.add_togroup("建筑",code,date="2022-05-04",vol=1000)

code = "sh.601012" #测试数据
kapi.add_togroup("建筑",code,date="2022-05-04",vol=1000)

code = "sh.601012" #测试数据

kapi.del_fromgroup("建筑",code,date="2022-05-04",vol=200)

code = "sz.003214" #测试数据
kapi.del_fromgroup("建筑",code,date="2022-05-04",vol=200)

resp = kapi.codes_fromgroup("建筑",start="2010-02-01",end="2022-10-15")
if isinstance(resp,list):
    for i in resp:
        print(i)
