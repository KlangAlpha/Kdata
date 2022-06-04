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
kapi = API()

# 系统会检查因子，不会重复创建
kapi.create_factor("macd",1,"标准macd指标")

macdcode=\
"""

kloop

Kl.date(start,end)
rdiff,rdea,rmacd = MACD(C)
callback(rdiff,rdea,rmacd)
endp
"""

result = []

##########################################################################
#
# 第一次执行
# 第一次执行数据较多，所以提交因子是按照每只股票提交一次
#
##########################################################################

start = '2021-08-03' # 获取200天之前的日期,约200个交易日
end   = get_date(0)  # 获取今天的日期

#Klang 执行的结果回调
def callback(rdiff,rdea,rmacd):
    global result 
    name,code = getstockinfo(0)
    result = []
    for i in range(len(rdiff)):
        
        macd = str(rdiff[i])+","+str(rdea[i])+","+str(rmacd[i])    
        result.append({"code":code,"macd":macd,"date":str(DATETIME[i])})
    print(code,name)
    # 每只股票提交一次
    kapi.post_factorb("macd",result)

Kexec(macdcode)

#############################################################################
# 日常更新
# 日常更新只更新 最后几天的数据
# 数据较少，所以采取一次性提交
##############################################################################

start = get_date(90) #获取90天之前的日期,约60交易日
end   = get_date(0)  # 获取今天的日期

#Klang 执行的结果回调
def callback(rdiff,rdea,rmacd):
    name,code = getstockinfo(0)

    for i in range(10):       
        macd = str(rdiff[i])+","+str(rdea[i])+","+str(rmacd[i])    
        result.append({"code":code,"macd":macd,"date":str(DATETIME[i])})

Kexec(macdcode)
# 提交B类 日更数据
kapi.post_factorb("macd",result)

#####################################################

print("macd 因子已经提交完成")



