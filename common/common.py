import argparse
import time
from datetime import datetime

#hostname = "http://127.0.0.1:1337/api"
hostname = "https://data.klang.org.cn/api"


parser = argparse.ArgumentParser()
parser.add_argument("--offset", help="开始执行的位置",default='0')
parser.add_argument("--endday", help="日期",default='0')
parser.add_argument("--start", help="日期",default='2021-01-01')

args = parser.parse_known_args()
if len(args) > 1:
    args = args[0]
offset = args.offset
endday = args.endday
start = args.start

today = datetime.now()
if endday == '0':
    endday = str(today.year) + str(today.month) + str(today.day)

def save_file(filename,content):
    f = open(filename,"w+")
    f.write(content)
    f.close()
