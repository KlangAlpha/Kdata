#
# volume ratio 量比
#

#
# 使用Klang 计算成交量 因子的例子，计算后提交到数据服务器
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
kapi.create_factor("volr",1,"量比，成交量比重10天，20天，30天")

volrcode=\
"""
kloop

Kl.date(start,end)
vol10=MA(V,10)
vol20=MA(V,20)
vol30=MA(V,30)
vr10 = V / vol10
vr20 = V / vol20
vr30 = V / vol30
callback(vr10,vr20,vr30)

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
def callback(vr10,vr20,vr30):
    global result 
    name,code = getstockinfo(0)
    result = []

    for i in range(len(vr10)):        
        volr = str(vr10[i])+","+str(vr20[i])+","+str(vr30[i])  
        result.append({"code":code,"volr":volr,"date":str(DATETIME[i])})
    print(code,name)
    # 每只股票提交一次
    kapi.post_factorb("volr",result)

if first:
    Kexec(volrcode)


#############################################################################
# 日常更新
# 日常更新只更新 最后几天的数据
# 数据较少，所以采取一次性提交
##############################################################################

start = get_date(400) # 获取
end   = get_date(0)  # 获取今天的日期

#Klang 执行的结果回调
def callback(vr10,vr20,vr30):
    name,code = getstockinfo(0)
    print(name,code,DATETIME)
    for i in range(10):       
        volr = str(vr10[i])+","+str(vr20[i])+","+str(vr30[i])  
        
        result.append({"code":code,"volr":volr,"date":str(DATETIME[i])})

if first == 0:
    Kexec(volrcode)
    # 提交B类 日更数据
    kapi.post_factorb("volr",result)

#####################################################

print("volr 因子已经提交完成")
