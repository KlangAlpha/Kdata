# Kdata
Klang data tools box.

数据提交服务器配置：common/common.py 默认值需要更改

# 功能
### 1. 为Klang 提供数据采集源头
   日K表：

    {'open': 15.01, 'close': 15.56, 'high': 15.59, 'low': 14.85, 'volume': 9946200.0, 'amount': 151293888.0, 'date': '2022-05-13', 'name': '中国国贸', 'code': 'sh.600007', 'turn': 0.9874} 
   

### 2. 计算因子 
   Klang 因子分定时更新和非定时更新，定时更新是日更。

   tdxhy.py 里有计算 板块的 不定时更新的因子的例子

   macd.py 里有 定时日更的例子，而且计算数据来源使用的是Klang本地数据源，第一次使用需要更新数据

   bs_pe.py 是从baostock 接口获取pe数据后提交到Klang 数据中心

### 3. 获取股票列表的例子：
```
from common.common import *
from common.framework import API

kapi = API() #klang data api
stocklist = kapi.get_stocklist().json()

for stock in stocklist:
    code ,name = stock['code'],stock['name']
```


任何问题请访问 https://forum.klang.org.cn 提问
