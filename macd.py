#
# 使用Klang 计算MACD 因子的例子，计算后提交到数据服务器
#

from Klang.lang import kparser,setPY,Kexec
from Klang import (Kl,Klang,
    C,O,V,H,L, CLOSE,HIGH,DATETIME,
    MA,CROSS,BARSLAST,HHV,COUNT,
    MAX,MIN,MACD)

Klang.Klang_init()

def getpyglobals(name):
    return globals().get(name)

def setpyglobals(name,val):
    globals()[name]=val


setPY(getpyglobals,setpyglobals)

def getstockinfo(default=0):
    return Kl.currentdf['name'] ,Kl.currentdf['code']

#####################################
# 以上为Klang引用可以直接复制以上内容
#####################################

from common.common import get_date
from common.framework import API

start = get_date(120) #获取120天之前的日期,约80交易日
end   = get_date(3)  # 获取今天的日期

result = []

#Klang 执行的结果回调
def callback(rdiff,rdea,rmacd):
    name,code = getstockinfo(0)

    
    for i in range(20):
        print(code,rdiff[i],rdea[i],rmacd[i],DATETIME[i])
        macd = str(rdiff[i])+","+str(rdea[i])+","+str(rmacd[i])    
        result.append({"code":code,"macd":macd,"date":str(DATETIME[i])})

macdcode=\
"""

kloop

Kl.date(start,end)
rdiff,rdea,rmacd = MACD(C)
callback(rdiff,rdea,rmacd)
endp
"""


Kexec(macdcode)

kapi = API()

# 系统会检查因子，不会重复创建
kapi.create_factor("macd",1,"标准macd指标")
# 提交B类 日更数据
kapi.post_factorb("macd",result)
print("macd 因子已经提交完成")

