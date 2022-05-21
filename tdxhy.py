#pytdx

import os
from pytdx.hq import TdxHq_API
import pandas as pd
from common.common import *
from common.framework import API
import json

parser.add_argument('--reset', type=int, default=0, help='reset data') 

args = parser.parse_known_args()
reset = args[0].reset

api = TdxHq_API()

serverip = '119.147.212.81'


tdxblockdf = ''
tdxblockex = ''

float2 = lambda a:float('%.2f' % a)



urls = [
        'http://www.tdx.com.cn/products/data/data/dbf/base.zip',
        'http://www.tdx.com.cn/products/data/data/dbf/gbbq.zip', # 如果从pytdx获取不到 incon.dat, 可以从本文件中再解压zhb.zip获得
]

codename = {}

#获取个股对应的板块名称
def QA_fetch_get_tdx_industry() -> pd.DataFrame:
    import random
    import tempfile
    import shutil
    import os
    from urllib.request import urlopen
    global tdxblockdf

    def gettempdir():
        tmpdir_root = tempfile.gettempdir()
        subdir_name = 'tdx_base' 
        tmpdir = os.path.join(tmpdir_root, subdir_name)
        if not os.path.exists(tmpdir): 
            os.makedirs(tmpdir)

        return tmpdir
 
    def download_tdx_file(tmpdir) -> str:
        
        #try:
            file = tmpdir + '/' + 'base.zip'
            f = urlopen(urls[0])
            data = f.read()
            with open(file, 'wb') as code:
                code.write(data)
            f.close()
            shutil.unpack_archive(file, extract_dir=tmpdir)
            os.remove(file)

            file = tmpdir + '/' + 'gbbq.zip'
            f = urlopen(urls[1])
            data = f.read()
            with open(file, 'wb') as code:
                code.write(data)
            f.close()
            shutil.unpack_archive(file, extract_dir=tmpdir)
            os.remove(file)
            file = tmpdir + '/' + 'zhb.zip'
            shutil.unpack_archive(file, extract_dir=tmpdir) 

        #except:
        #    pass
            return tmpdir

    def read_industry(folder:str) -> pd.DataFrame:
        incon = folder + '/incon.dat' # tdx industry file
        
        hy = folder + '/tdxhy.cfg' # tdx stock file

        tbk = {}
        # tdx industry file
        with open(incon, encoding='GB18030', mode='r') as f:
            incon = f.readlines()
        incon_dict = {}
        for i in incon:
            if i[0] == '#' and i[1] != '#':
                j = i.replace('\n', '').replace('#', '')
                incon_dict[j] = []
                start = 1
            else:
                if i[1] != '#':
                    codelist = i.replace('\n', '').split(' ')[0].split('|')
                    if len(codelist[0]) == 5 and codelist[0][0] == 'T':
                        tbk[codelist[0]] = codelist[1]

                    incon_dict[j].append(i.replace('\n', '').split(' ')[0].split('|'))

        incon = pd.concat([pd.DataFrame.from_dict(v).assign(type=k) for k,v in incon_dict.items()]) \
            .rename({0: 'code', 1: 'name'}, axis=1).reset_index(drop=True)
        
        with open(hy, encoding='GB18030', mode='r') as f:
            hy = f.readlines()
        hy = [line.replace('\n', '') for line in hy]
        hy = pd.DataFrame(line.split('|') for line in hy)
        
        # filter codes
        hy = hy[~hy[1].str.startswith('9')]
        hy = hy[~hy[1].str.startswith('2')]

        hy1 = hy[[1, 2]].set_index(2).join(incon.set_index('code')).set_index(1)[['name', 'type']]
        hy2 = hy[[1, 5]].set_index(5).join(incon.set_index('code')).set_index(1)[['name', 'type']]
        #print(hy1)
        #print(hy2)
        # add 56 tdx block
        count = 0
        hy['tbk1'] = ""
        for i in hy[2].values:
            if len(i) >=5:
                hy['tbk1'].iloc[count] = tbk[i[:5]]
            count += 1

        # join tdxhy and swhy
        df = hy.set_index(1) \
            .join(hy1.rename({'name': hy1.dropna()['type'].values[0], 'type': hy1.dropna()['type'].values[0]+'_type'}, axis=1)) \
            .join(hy2.rename({'name': hy2.dropna()['type'].values[0], 'type': hy2.dropna()['type'].values[0]+'_type'}, axis=1)).reset_index()

        df.rename({0: 'sse', 1: 'code', 2: 'TDX_code', 3: 'SW_code'}, axis=1, inplace=True)
        df = df[[i for i in df.columns if not isinstance(i, int) and  '_type' not in str(i)]]
        df.columns = [i.lower() for i in df.columns]

        return df
    folder = gettempdir()
    if reset != 0:
        shutil.rmtree(folder, ignore_errors=True)
    dirpath = folder
    if not os.path.exists(folder + '/incon.dat') or not os.path.exists(folder + '/tdxhy.cfg'): 
        print("Save file to ",folder)
        download_tdx_file(folder)
    
    if len(tdxblockdf ) < 1000:
        print("Read file from ",folder)
        df = read_industry(folder)
        tdxblockdf = df


codebuffer={}


#初始化 ,并获取概念板块名称
api.connect(serverip, 7709)

# 偶尔出现 gn加载不成功的情况
try:
    b = api.get_and_parse_block_info('block_gn.dat')
except:
    b = api.get_and_parse_block_info('block_gn.dat')
    
hy1 = pd.DataFrame(b)


# 获取板块
QA_fetch_get_tdx_industry()
hy = tdxblockdf
hydict = {}
hy1dict = {}
print(hy)


#个股对应板块名的表

for i in range(0,len(hy)):
    sse = hy.sse.iloc[i]
    code = hy.code.iloc[i]
    bkname = hy.tdxnhy.iloc[i]
    hydict[code] = [bkname,sse]
print("block : ",len(hy)," ",len(hydict.keys()))
#个股对应概念板块的表

for i in range(0,len(hy1)):
    code = hy1.code.iloc[i]
    bkname = hy1.blockname.iloc[i]
    if hy1dict.get(code):
        hy1dict[code].append(bkname)
    else:
        hy1dict[code] = [bkname]

print("gn : ",len(hy1), " ", len(hy1dict.keys()))

# 0 is name, 1 is sse
def getmarket(code):
    if hydict.get(code):
        return hydict[code][1]
    elif int(code)>=600000:
        return 1
    elif int(code)<600000:
        return 0

def gettdxbk(code):
    code = code.split('.')[1]
    return hydict.get(code,[""])[0]

def gettdxgn(code):
    code = code.split('.')[1]
    return hy1dict.get(code,[""])


    
#tdx 板块信息只有 个股code对应板块名
#因此要获取code和股票名的 对应表
kapi = API() #klang data api
stocklist = kapi.get_stocklist().json()


    

api.connect(serverip, 7709)
if __name__ == "__main__":
    factor1 = []
    factor2 = []
    for i in stocklist:
        
        bk = gettdxbk(i['code'])
        gn = gettdxgn(i['code'])
        gn = ",".join(gn)
        print(i['code'],i['name'],bk,gn)
        factor1.append({'code':i['code'],"value":bk})
        factor2.append({'code':i['code'],"value":gn})
    
    kapi.create_factor("tdxbk",0,"通达信板块")
    kapi.post_factora("tdxbk",factor1)
    kapi.create_factor("tdxgn",0,"通达信概念")
    kapi.post_factora("tdxgn",factor2)
