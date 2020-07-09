import requests
import json
import pandas as pd
import os
import time


def getHTMLText(url, code='utf-8'):
    '''
    下载股票内容， 使用api接口，
    http://71.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408232575596603897_1594245828281&pn=1&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1594245828282
    pz20 为20条， pz30为30条
    修改 pz4035， 抓取所有A股内容
    '''
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.63 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return ''

def getStockInfo(url,lst):
    '''
    分析抓取股票内容储存到一个list
    '''
    html = getHTMLText(url)
    stock_start = html.find('[')
    stock_end = html.find(']')
    stock_info = json.loads(html[stock_start : stock_end+1])#get the stock info
    '''
    # f2最新价 f3涨跌幅 f4涨跌额 f5成交量 f6成交额 f7振幅  f8换手率 f9市盈率 f10量比 
    f12代码  f14名称  f15最高价  f16最低  f17今开 f18昨收  f23 市净率
    '''
    for stock in stock_info:
        feature= [
            stock['f12'],
            stock['f14'],
            stock['f2'],
            stock['f3'],
            stock['f4'],
            stock['f5'],
            stock['f6'],
            stock['f7'],
            stock['f15'],
            stock['f16'],
            stock['f17'],
            stock['f18'],
            stock['f10'],
            stock['f8'],
            stock['f9'],
            stock['f23']
        ]
        lst.append(feature)


def save_data(path, lst):
    '''
    f2最新价 f3涨跌幅 f4涨跌额 f5成交量 f6成交额 f7振幅  f8换手率 f9市盈率 f10量比
    f12代码  f14名称  f15最高价  f16最低  f17今开 f18昨收  f23 市净率
    '''
    col_names = ['股票代码', '名称', '最新价', '涨跌幅',
                 '涨跌额', '成交量', '成交额',
                 '振幅', '最高价', '最低价',
                 '今开', '昨收', '量比',
                 '换手率', '市盈率', '市净率']
    df = pd.DataFrame(lst, columns=col_names)
    file_dir = path  # enter the file location
    file_name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10]+'.csv'
    file = os.path.join(file_dir, file_name)
    try:
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        if not os.path.exists(file):
            df.to_csv(file)
            print('load success')
        else:
            print('file exist')
    except:
        print('load failed')

def main():
    path = 'C:\\Users\\User\\Desktop\\project\\stock'
    stock=[]
    url = 'http://71.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408232575596603897_1594245828281&pn=1&pz=4035&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1594245828282'
    getStockInfo(url, stock)
    save_data(path, stock)


if __name__=='__main__':
    main()

