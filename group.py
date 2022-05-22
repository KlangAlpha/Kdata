#
# Kdata 组接口
#
from common.framework import API

kapi = API()

kapi.create_group("建筑","目前建筑板块正在启动")

#code = "sh.601012" #测试数据
code = "sz.003214" #测试数据
kapi.add_togroup("建筑",code,date="2022-05-03",vol=1000)

code = "sh.601012" #测试数据
kapi.add_togroup("建筑",code,date="2022-05-03",vol=1000)

code = "sh.601012" #测试数据

kapi.del_fromgroup("建筑",code,date="2022-05-04",vol=200)

code = "sz.003214" #测试数据
kapi.del_fromgroup("建筑",code,date="2022-05-04",vol=200)

#resp = kapi.get_group("高领持仓",start="2003-02-01",end="2021-10-15")
