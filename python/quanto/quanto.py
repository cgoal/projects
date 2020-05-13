# -*- coding: utf-8 -*-


import os
import numpy as np
import pandas as pd
import baostock as bs
import time
import sys

def iniParams(code='sh.000001',sd='2015-01-01',ed='',fr='d',af='2'):
    
    if ed=='':
        localtime=time.localtime()
        ed=str(localtime.tm_year)+'-'+('00'+str(localtime.tm_mon))[-2:]+'-'+('00'+str(localtime.tm_mday))[-2:]
    
    params={}
    params['code']=code
    params['fields']='date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST'
    params['startdate']=sd
    params['enddate']=ed
    params['frequency']=fr
    params['adjustflag']=af
    
    return params


def realtime(stocks='sh.600000,sz.000001'):
    lr=bs.login_real_time()
    
    if lr.error_code!='0':
        return 'login error' + lr.error_msg
    
    rs=bs.subcribe_by_code(stocks,0,cbFunc,'','user_params')
    if rs.error_code!='0':
        print(rs.error_msg)
    else:
        text=input('press any key to stop\r\n')
        cancel_rs=bs.cancel_subscribe(rs.serial_id)
    
    lr=bs.logout_real_time()

def cbFunc(data):
    
    print(data)

def analysis():
    
    pass




def main():
    lg=bs.login()
    
    if lg.error_code!='0':
        sys.exit(0)
    
    #个股数据
    for c in ['sh.000001','sz.399001','sz.399006','sh.000012','sh.000013']:
        p=iniParams(code=c)
        rs=bs.query_history_k_data(p['code'],
                               p['fields'],
                               p['startdate'],
                               p['enddate'],
                               p['frequency'],
                               p['adjustflag'])
    
        data=[]
        while (rs.error_code=='0') & rs.next():
            data.append(rs.get_row_data())
        
        idata=pd.DataFrame(data, columns=rs.fields)
        idata.to_csv(c+'_data.csv')
    
    #货币供应量
    rs=bs.query_money_supply_data_month(start_date='2009-01')
    data=[]
    while (rs.error_code=='0') & rs.next():
        data.append(rs.get_row_data())
        
    mdata=pd.DataFrame(data,columns=rs.fields)
    mdata.to_csv('mdata.csv')
    
    #shibor
    rs=bs.query_shibor_data(start_date=p['startdate'])
    data=[]
    while (rs.error_code=='0') & rs.next():
        data.append(rs.get_row_data())
        
    shibor=pd.DataFrame(data,columns=rs.fields)
    shibor.to_csv('shibor.csv')
    
    
    
    
    bs.logout()
            
if __name__=="__main__":
    
    main()