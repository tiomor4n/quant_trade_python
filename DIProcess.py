# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:37:04 2016

@author: simon
"""

def DIProcess(vTarget):
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
    from DataPipe import TWNStockTIOMO,YahooFinance
    from figure_plot_output import Acct_mkt_compare,Acct_mkt_candle
    from ClsGenReport import CalCAGR,CalSharpInd,CalDD,BackwardTest
    
    dealArr = YahooFinance(vTarget=vTarget)
    #dealArr = TWNStockTIOMO(vTarget=vTarget,vbegin = '201101',vend = '201512')
    Cind = IndexCal(dealArr)
    '''
    用DI+ > DI-做多，DI- <DI+做空，用prebadK停損
    '''
    RecDateArr=[]
    RecAmtArr=[]
    RecContArr=[]
    ClosePriceArr = []
    CloseConArr = []   
    RsiArr = []
    maArr = []
    
    
    
    lenw = 17
    i = 0
    preDIp = -1
    preDIm = -1
    newDIp = -1
    newDIm = -1
    PostAmt = 1
    Acct1 = Account(initAmt = 400000.)
    
    RsiArr = Cind.RsiCal(lenw)
    maArr = Cind.moving_average(Cind.ClosePriceArr,40)

    
    upCriteria = 70
    downCriteria = 30
    #因為不會有負值，用-1當作初始值
    for deal in dealArr:
        Acct1.BuildArr.append(None)
        Acct1.EvenArr.append(None)
        ind = Cind.dateArr.index(deal.TradeDate)
        
        preMA = maArr[ind-1]
        nowMA = maArr[ind]
        for cont in Acct1.UnConList:
            cont.OverDate(deal)                    
            
            if cont.TradeWay > 0:
                rTrend = 'UP'
            else:
                rTrend = 'DOWN'
           
            
            
            if cont.StopLoss_FixPer(N = 0.05):
                cont.CloseContract(deal)
                Acct1.AcctCloseCon()
                Acct1.totalAmt = Acct1.totalAmt + floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
                CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice,'Stop Loss':'Yes'})
                print 'Init Date: ' + date2str(cont.InitDate) + ' Init Price:' + str(cont.BuildPrice) +' stop price:' + str(cont.EvenPrice) +\
                ' exit at:' + date2str(deal.TradeDate) + ' TredeWay:' + str(cont.TradeWay) + ' stoploss:Y'
            
            
            
            
                
            if cont.TradeWay > 0:                     
                if Cind.RsiStop(vDeal = deal,vTrend = rTrend,Criteria = upCriteria,vRsiArr = RsiArr,vwindow=lenw):
                    cont.CloseContract(deal)
                    Acct1.AcctCloseCon()
                    Acct1.totalAmt = Acct1.totalAmt + floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
                    CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice,'Stop Loss':'Yes'})
                    print 'Init Date: ' + date2str(cont.InitDate) + ' Init Price:' + str(cont.BuildPrice) +' stop price:' + str(cont.EvenPrice) +\
                    ' exit at:' + date2str(deal.TradeDate) + ' TredeWay:' + str(cont.TradeWay)+ ' stoploss:N'
                        
            else:            
                if Cind.RsiStop(vDeal = deal,vTrend = rTrend,Criteria = downCriteria,vRsiArr = RsiArr,vwindow=lenw):
                    cont.CloseContract(deal)
                    Acct1.AcctCloseCon()
                    Acct1.totalAmt = Acct1.totalAmt + floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
                    CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice,'Stop Loss':'Yes'})
                    print 'Init Date: ' + date2str(cont.InitDate) + ' Init Price:' + str(cont.BuildPrice) +' stop price:' + str(cont.EvenPrice) +\
                    ' exit at:' + date2str(deal.TradeDate) + ' TredeWay:' + str(cont.TradeWay)+ ' stoploss:N'
            
                
                
        RecDateArr.append(deal.TradeDate)
        RecAmtArr.append(Acct1.totalAmt)
        ClosePriceArr.append(deal.ClosePrice)
        
        if i <= lenw:
            i += 1
            continue
        else:
            if newDIp == -1 and newDIm == -1:
                newDIp,newDIm = Cind.DICal(vDeal = deal)
                continue                
            else:
                preDIp = newDIp
                preDIm = newDIm
                newDIp,newDIm = Cind.DICal(vDeal = deal)
                if (preDIp - preDIm)* (newDIp - newDIm)<0:
                    if nowMA < preMA:
                        if (preDIp - preDIm) > 0:
                            #continue
                            #做空
                            cont1 = Contract(ContName=date2str(deal.TradeDate),Position = PostAmt*1000,vDateDeal = deal,TradeWay=-1)
                            Acct1.AddContr(cont1)
                            #print 'preDIp:' + str(preDIp) + ' preDIm:' + str(preDIm) +' newDIp:' + str(newDIp)+ ' newDIm:' + str(newDIm)
                    else:
                        if preMA < nowMA:
                            #做多
                            #continue
                            cont1 = Contract(ContName=date2str(deal.TradeDate),Position = PostAmt*1000,vDateDeal = deal,TradeWay=1)
                            Acct1.AddContr(cont1)
                            #print 'preDIp:' + str(preDIp) + ' preDIm:' + str(preDIm) +' newDIp:' + str(newDIp)+ ' newDIm:' + str(newDIm) 
            
                    
    #Acct_mkt_compare(RecDateArr,RecAmtArr,ClosePriceArr)   
    Acct_mkt_candle(dealArr,RecAmtArr,Acct1.BuildArr)

    rCalDDAmt,rCalDD = CalDD(RecAmtArr)
    printtxt = []
    printtxt.append('CARG:' + txtpercent(CalCAGR(RecAmtArr)))
    printtxt.append('Sharp Index:' + txtpercent(CalSharpInd(RecAmtArr)))
    printtxt.append('Max DD duration:' + str(rCalDD))
    printtxt.append('Max DD Amount:' + txtpercent(rCalDDAmt))
    printtxt.append('Target:' + vTarget)
    
    BackwardTest("test.png",printtxt) 

                
            
DIProcess(vTarget='2498.TW')       
    
    
    