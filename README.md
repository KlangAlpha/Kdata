# Kdata
Klang data tools box.

# 功能
### 1. 为Klang 提供数据采集源头
   日K表：

    {'open': 15.01, 'close': 15.56, 'high': 15.59, 'low': 14.85, 'volume': 9946200.0, 'amount': 151293888.0, 'date': '2022-05-13', 'name': '中国国贸', 'code': 'sh.600007', 'turn': 0.9874} 
   
   所属行业表:

   以baostock库为模版，增加了通达信的56个板块和gn板块，还有筹码值

    ['updateDate', 'code', 'code_name', 'industry', 'industryClassification','tdxbk','tdxgn','chouma']

### 2. 计算因子 
   Klang 因子分定时更新和非定时更新，定时更新是日更。

   tdxhy.py 里有计算 板块的 不定时更新的因子的例子

   macd.py 里有 定时日更的例子，而且计算指标使用的是Klang

任何问题请访问 https://forum.klang.org.cn 提问
