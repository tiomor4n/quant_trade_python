# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:59:13 2015

@author: simon
"""
import csv
import datetime
import strategy1
from strategy1 import IndexCal
import math
from BaseFunction import date2str,floatrou,str2date,txtpercent
from ClsContract import Account
from ClsContract import Contract
from ClsContract import DateDeal
from strategy1 import durationMax
from strategy1 import IndexCal
from DataPipe import TWNStockTIOMO
from figure_plot_output import Acct_mkt_compare,Acct_mkt_candle
from ClsGenReport import CalCAGR,CalSharpInd,CalDD,BackwardTest

PostAmt = 1000
dealArr = []

RecDateArr=[]
RecAmtArr=[]
RecContArr=[]
ClosePriceArr = []
DateATRArr=[]
ATRArr = []
CloseConArr = []

def ParameterChg():
    rtestItem = raw_input(">>> Please input testItem: ")
    rtestYear1 = raw_input(">>> Please input testYear1: ")
    rtestYear2 = raw_input(">>> Please input testYear2: ")
    
    
    return rtestItem,rtestYear1,rtestYear2
    
rItem,rTestYear1,rTestYear2 = ParameterChg()

dealArr = TWNStockTIOMO(vTarget = rItem,vbegin = rTestYear1,vend= rTestYear2)
   
IndCal = IndexCal(dealArr)
ATRArr,DateATRArr = IndCal.ATRCal()
struMA = IndCal.MACal()


Acct1 = Account(initAmt = 400000.)
dura = durationMax(dealArr)


i=0

for deal in dealArr:
    i += 1
    for cont in Acct1.UnConList:
        cont.OverDate(deal)
        #print cont.ContName + ':' + date2str(deal.TradeDate) + ":" + str(cont.HoldDuration)
    for cont in Acct1.UnConList:
        if(cont.HoldDuration==20):
            #print cont.ContName + ' End at:' + date2str(deal.TradeDate)            
            cont.CloseContract(deal)            
            Acct1.AcctCloseCon()
            '''
            計算手續費，買賣時都須加計交易金額*0.001425
            計算手續費，賣出時須加計交易金額*0.003
            '''
            Acct1.totalAmt = Acct1.totalAmt - floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
            CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice})
            #print cont.ContName + ' GainLoss:' + str(cont.GainLoss)
        
            
    RecDateArr.append(deal.TradeDate)
    RecAmtArr.append(Acct1.totalAmt)
    ClosePriceArr.append(deal.ClosePrice)
    
    '''
    找該date之ATR，然後計算該日如果交易的最適交易量
    ''' 
    if deal.TradeDate in DateATRArr:
        IntATR = DateATRArr.index(deal.TradeDate)+1    
        ATR = ATRArr[IntATR]
        PostAmt = math.floor((Acct1.totalAmt * 0.01)/(ATR*1000))
    else:
        continue
    
    '''
    加上MA位置filter
    '''
    if IndCal.MAPosition(vRange=60,vDeal = deal,vLocate = 'DOWN'):
        continue
    
    if(dura.CalMax(vTargetDate = date2str(deal.TradeDate),Period = 10)):
        if len(Acct1.UnConList)<4:
            cont1 = Contract(ContName=date2str(deal.TradeDate),Position = PostAmt*1000,vDateDeal = deal)
            Acct1.AddContr(cont1)
            '''
            計算手續費，買賣時都須加計交易金額*0.001425
            '''
            Acct1.totalAmt = Acct1.totalAmt - floatrou(cont1.BuildPrice * cont1.Position * 0.001425 * 0.06)
            RecContArr.append(cont1)

#print len(dealArr)
#print len(RecAmtArr)
#print IndCal.dealarr[0].TradeDate
#print dealArr[0].TradeDate
#print RecDateArr[0]
            
#Acct_mkt_compare(RecDateArr,RecAmtArr,ClosePriceArr)   
Acct_mkt_candle(dealArr,RecAmtArr)

rCalDDAmt,rCalDD = CalDD(RecAmtArr)
printtxt = []
printtxt.append('CAGR:' + txtpercent(CalCAGR(RecAmtArr)))
printtxt.append('CalSharpInd:' + txtpercent(CalSharpInd(RecAmtArr)))
printtxt.append('CalDD:' + str(rCalDD))
printtxt.append('CalDDAmt:' + txtpercent(rCalDDAmt))

BackwardTest("test.png",printtxt)         

for ar in CloseConArr:
   print 'InitDate:'  + date2str(ar['InitDate']) + ', EndDate:' + date2str(ar['EndDate']) + ',DealAmt:' + str(ar['DealAmt']) + ',OpenPrice:'\
   + str(ar['OpenPrice']) + ',ClosePrice:' + str(ar['ClosePrice'])
   