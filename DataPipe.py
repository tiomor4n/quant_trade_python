# -*- coding: cp950 -*-
"""
Created on Sat Dec 19 08:27:08 2015

@author: simon
"""

from ClsContract import DateDeal
from BaseFunction import date2str
from BaseFunction import str2date
from BaseFunction import floatrou
import datetime
import csv
import sys
import os
import urllib2
from bs4 import BeautifulSoup as bs
import json


def TWNFutureLocal(vYear,vItem):
    
    def movedash(vstr='',vkind = 'float'):
        try:
            a = float(vstr)
            if vkind == 'float':
                return float(a)
            elif vkind == 'int':
                return int(a)
        except ValueError:
            return 0
    
    dealArr = []    
    settledatearr=[]
       
    settleDTroute = os.path.join(os.getcwd(),vYear + 'setttledate.csv')  
    dataroute = os.path.join(os.getcwd(),vYear + '_fut.csv')  
    
    with open(settleDTroute) as csvsedtfile:
        reader = csv.DictReader(csvsedtfile)
        for row in reader:
            settledatearr.append(str2date(row['date']))    
    
    with open(dataroute) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['契約'] == vItem:
                try:    
                    dDeal = DateDeal(TradeDate = str2date(row['交易日期'],'%Y/%m/%d'),                          
                              OpenPrice = movedash(row['開盤價']),
                              HighPrice = movedash(row['最高價']),
                              LowPrice = movedash(row['最低價']),
                              ClosePrice = movedash(row['收盤價']),
                              DealAmt = movedash(row['成交量']),
    
                             
                    )
                except ValueError:
                    print 'please check contract ' + row['契約'] + ' ' + date2str(str2date(row['交易日期']))
                    sys.exit()
                        
                '''
                判斷是否為近一月契約
                '''
                ContDate = row['到期月份(週別)']
                #FutTradeDate = dDeal.TradeDate
                
                if ContDate == vYear + '01' and (datetime.datetime(int(vYear),1,1)<=dDeal.TradeDate <= settledatearr[0]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '02' and (settledatearr[0] < dDeal.TradeDate <= settledatearr[1]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '03' and (settledatearr[1] < dDeal.TradeDate <= settledatearr[2]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '04' and (settledatearr[2] < dDeal.TradeDate <= settledatearr[3]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '05' and (settledatearr[3] < dDeal.TradeDate <= settledatearr[4]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '06' and (settledatearr[4] < dDeal.TradeDate <= settledatearr[5]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '07' and (settledatearr[5] < dDeal.TradeDate <= settledatearr[6]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '08' and (settledatearr[6] < dDeal.TradeDate <= settledatearr[7]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '09' and (settledatearr[7] < dDeal.TradeDate <= settledatearr[8]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '10' and (settledatearr[8] < dDeal.TradeDate <= settledatearr[9]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '11' and (settledatearr[9] < dDeal.TradeDate <= settledatearr[10]):
                    dealArr.append(dDeal)
                if ContDate == vYear + '12' and (settledatearr[10] < dDeal.TradeDate <= settledatearr[11]):
                    dealArr.append(dDeal)
                
    return dealArr
    
    
def TWNStockLocal():
    dealArr = []
    with open(r'D:\Program\python\testzone\TW_Stock_Indi.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dDeal = DateDeal(TradeDate = str2date(row['TxnDate'],'%m/%d/%Y'),
                             OpenPrice = float(row['OpenPrice']),
                             HighPrice = float(row['HighPrice']),
                             LowPrice = float(row['LowPrice']),
                             ClosePrice = float(row['ClosePrice']),
                             DealAmt = float(row['DealStockAmt'])
            )
            dealArr.append(dDeal)
    return dealArr
            
            
def TWNStockTIOMO(vTarget = '2330',vbegin='201501',vend='201512'):
    urlToVisit = 'http://tiomo.somee.com/TWSPAPI/showdata?strStockCode='+ vTarget + '&strDataDate=' + vbegin + '&strEndDate=' + vend
    #urlToVisit = 'http://tiomo.somee.com/TWSPAPI/showdata?strStockCode=2330&strDataDate=201501&strEndDate=201512'
    sourceCode = urllib2.urlopen(urlToVisit)
    soup = bs(sourceCode.read())
    jsontxt = soup.find('body').text.replace('\r','').replace('\n','').replace(' ','')
    config = json.loads(jsontxt)
    dealArr = []
    for a in config:
        dDeal = DateDeal(TradeDate = str2date(a['TxnDate'],'%m/%d/%Y'),
                             OpenPrice = floatrou(a['OpenPrice']),
                             HighPrice = floatrou(a['HighPrice']),
                             LowPrice = floatrou(a['LowPrice']),
                             ClosePrice = floatrou(a['ClosePrice']),
                             DealAmt = floatrou(a['DealStockAmt'])
            )
        dealArr.append(dDeal)
    return dealArr
