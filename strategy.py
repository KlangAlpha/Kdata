#
# Klang 策略创建例子
#

from common.framework import API


kapi = API()

content="""
diff,dea,macd=MACD(C)
buy=CROSS(diff,dea)
sell=CROSS(dea,diff)
"""

kapi.create_strategy(
    "MACD金叉买卖",
    content,
    "通过 计算 macd 金叉购买，死叉卖出",
    1,
    "Klang"
)


content="""
diff,dea,macd = get_factor('macd')
buy=CROSS(diff,dea)
sell=CROSS(dea,diff)
"""

kapi.create_strategy(
    "MACD金叉买卖1",
    content,
    "通过 计算 macd 金叉购买，死叉卖出数据来自因子数据库",
    1,
    "Klang"
)

resp = kapi.get_strategy({"lang":"Klang","status":1})
print(resp.content)
