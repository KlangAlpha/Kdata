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

from Kdata import get_date 
from Kdata import API #次调用为安装后的Kdata函数
kapi = API()

# 系统会检查因子，不会重复创建
kapi.create_factor("ma",1,"常用均线,支持MA5,10,20,30,60,120,250")

macode=\
"""
kloop

Kl.date(start,end)
ma5=MA(C,5)
ma10=MA(C,10)
ma20=MA(C,20)
ma30=MA(C,30)
ma60=MA(C,60)
ma120=MA(C,120)
ma250=MA(C,250)
callback(ma5,ma10,ma20,ma30,ma60,ma120,ma250)

endp
"""

result = []

first = 0 #第一次设置 first = 1，以后升级数据，设置first = 0

##########################################################################
#
# 第一次执行
# 第一次执行数据较多，所以提交因子是按照每只股票提交一次
#
##########################################################################


start = '2020-01-01' # 获取
end   = get_date(0)  # 获取今天的日期

#Klang 执行的结果回调
def callback(ma5,ma10,ma20,ma30,ma60,ma120,ma250):
    global result 
    name,code = getstockinfo(0)
    result = []

    for i in range(len(ma5)):        
        ma = str(ma5[i])+","+str(ma10[i])+","+str(ma20[i])+","+str(ma30[i])\
            +","+str(ma60[i])+","+str(ma120[i])+","+str(ma250[i])   
        result.append({"code":code,"ma":ma,"date":str(DATETIME[i])})
    print(code,name)
    # 每只股票提交一次
    kapi.post_factorb("ma",result)

if first:
    Kexec(macode)


#############################################################################
# 日常更新
# 日常更新只更新 最后几天的数据
# 数据较少，所以采取一次性提交
##############################################################################

start = get_date(400) # 获取
end   = get_date(0)  # 获取今天的日期

#Klang 执行的结果回调
def callback(ma5,ma10,ma20,ma30,ma60,ma120,ma250):
    name,code = getstockinfo(0)
    print(name,code,ma250,DATETIME)
    for i in range(10):       
        ma = str(ma5[i])+","+str(ma10[i])+","+str(ma20[i])+","+str(ma30[i])\
            +","+str(ma60[i])+","+str(ma120[i])+","+str(ma250[i])   
        result.append({"code":code,"ma":ma,"date":str(DATETIME[i])})

if first == 0:
    Kexec(macode)
    # 提交B类 日更数据
    kapi.post_factorb("ma",result)

#####################################################

print("ma 因子已经提交完成")
