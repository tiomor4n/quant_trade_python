# -*- coding: cp950 -*-
import sys
import os
from ClsContract import DateDeal
from ClsContract import Account
from ClsContract import Contract
from BaseFunction import date2str,writetxt,txtpercent,floatrou
import datetime
from strategy1 import IndexCal
from DataPipe import TWNFutureLocal
from figure_plot_output import Acct_mkt_compare
from ClsGenReport import CalCAGR,CalSharpInd,CalDD,BackwardTest


def OneDayTransaction(TType='Open',vDeal = DateDeal,vTradeWay = 1,vStopLossPt = 10,vflexP = 1,vPosition=0):
       
    if TType == 'Open':
        Cont = Contract(vDateDeal = vDeal,OpenApp = 'Open',TradeWay = vTradeWay, Position = vPosition,ContName = date2str(vDeal.TradeDate))
        if vTradeWay >0:
            if vDeal.OpenPrice - vDeal.LowPrice >= vStopLossPt:  #要停損
                result = max(vDeal.OpenPrice - vStopLossPt - vflexP,vDeal.LowPrice)
                Cont.CloseContract(vDateDeal= vDeal,ClosePrice = result,CloseApp = 'Assign')
            else:
                Cont.CloseContract(vDateDeal= vDeal,CloseApp = 'Close')            
        else:
            if vDeal.HighPrice - vDeal.OpenPrice >= vStopLossPt:  #要停損
                result = min(vDeal.OpenPrice + vStopLossPt + vflexP,vDeal.HighPrice)
                Cont.CloseContract(vDateDeal= vDeal,ClosePrice = result,CloseApp = 'Assign')
            else:
                Cont.CloseContract(vDateDeal= vDeal,CloseApp = 'Close')  

            
        
    return Cont
        
    
def ParameterChg():
    rtestYear = raw_input(">>> Please input testYear: ")
    rtestItem = raw_input(">>> Please input testItem: ")
    return rtestYear,rtestItem
    

def movedash(vstr='',vkind = 'float'):
    try:
        a = float(vstr)
        if vkind == 'float':
            return float(a)
        elif vkind == 'int':
            return int(a)
    except ValueError:
        return 0
        
def feeCal(vPt= 0.,vPosition= 0,vfee=0.):
    return round(vPt * Position * (2/100000)) + vfee
        

dealArr = []
settledatearr=[]
DayResult1Arr = []
DayResult2Arr = []
RecDateArr = []
RecAmt1Arr = []
RecAmt2Arr = []
ClosePriceArr = []
totalAmtArr = []
ContDate = ''
FutTradeDate = datetime.datetime(2000,1,1)
PrePrice = 0.
NowPrice = 0.
Position=0


testYear,testItem = ParameterChg()
if (testYear == '' or testItem == ''):
    print 'please insert Year and Item'
    sys.exit()
    
if testItem == 'MTX':
    Position = 50
elif testItem == 'TX':
    Position = 200

Acct1 = Account(initAmt = 200000.)
Acct2 = Account(initAmt = 200000.)
if os.path.isfile('AA.txt'):
    writetxt('AA.txt','tradedate' + ','+ 'BuildPrice' + ',' + 'EvenPrice' + ',' + 'GainLoss'+ ','+ 'AcctAmt' )

dealArr = TWNFutureLocal(testYear,testItem)
            
IC = IndexCal(dealArr)
for i in range(len(dealArr)):
    if i == 0:
        continue
    else:
        PrePrice = dealArr[i-1].ClosePrice
        NowPrice = dealArr[i].ClosePrice
        ClosePriceArr.append(NowPrice)
        RecDateArr.append(dealArr[i].TradeDate)
        
        '''
        季線位置策略
        '''        
        if IC.MAPosition(vRange=60,vDeal = dealArr[i],vLocate = 'DOWN'):
            RecAmt1Arr.append(Acct1.totalAmt)
            RecAmt2Arr.append(Acct2.totalAmt)
            totalAmtArr.append(Acct1.totalAmt + Acct2.totalAmt)
            continue
        
        '''
        當沖策略
        '''
        DayResult1 = OneDayTransaction(vDeal = dealArr[i],vTradeWay = 1,vPosition = Position)   #這是一個Contract
        DayResult1Arr.append(DayResult1)
        Acct1.AddContr(DayResult1)
        Acct1.AcctCloseCon()
        Acct1.totalAmt =  Acct1.totalAmt - feeCal(vPt=dealArr[i].ClosePrice,vPosition = Position,vfee=60)
        RecAmt1Arr.append(Acct1.totalAmt)
        
        DayResult2 = OneDayTransaction(vDeal = dealArr[i],vTradeWay = -1,vPosition = Position)   #這是一個Contract
        DayResult2Arr.append(DayResult2)
        Acct2.AddContr(DayResult2)
        Acct2.AcctCloseCon()
        Acct2.totalAmt = Acct2.totalAmt - feeCal(vPt=dealArr[i].ClosePrice,vPosition = Position,vfee=60)
        RecAmt2Arr.append(Acct2.totalAmt)
        totalAmtArr.append(Acct1.totalAmt + Acct2.totalAmt)

        
        writetxt('AA.txt',date2str(dealArr[i].TradeDate) + ','+ str(DayResult1.BuildPrice) + ',' + str(DayResult1.EvenPrice)\
                 + ',' + str(DayResult1.GainLoss) + ','+ str(Acct1.totalAmt))
        

  
Acct_mkt_compare(RecDateArr,RecAmt2Arr,ClosePriceArr)

rCalDDAmt,rCalDD = CalDD(totalAmtArr)
printtxt = []
printtxt.append('CAGR:' + txtpercent(CalCAGR(totalAmtArr)))
printtxt.append('CalSharpInd:' + txtpercent(CalSharpInd(totalAmtArr)))
printtxt.append('CalDD:' + str(rCalDD))
printtxt.append('CalDDAmt:' + txtpercent(rCalDDAmt))

BackwardTest("test.png",printtxt)

