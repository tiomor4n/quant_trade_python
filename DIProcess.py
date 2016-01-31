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
    from figure_plot_output import Acct_mkt_compare
    from ClsGenReport import CalCAGR,CalSharpInd,CalDD,BackwardTest
    
    dealArr = YahooFinance(vTarget=vTarget)
    Cind = IndexCal(dealArr)
    '''
    用DI+ > DI-做多，DI- <DI+做空，用prebadK停損
    '''
    RecDateArr=[]
    RecAmtArr=[]
    RecContArr=[]
    ClosePriceArr = []
    CloseConArr = []    
    
    lenw = 14
    i = 0
    preDIp = -1
    preDIm = -1
    newDIp = -1
    newDIm = -1
    PostAmt = 1
    Acct1 = Account(initAmt = 400000.)
    
    upCriteria = 70
    downCriteria = 30
    #因為不會有負值，用-1當作初始值
    for deal in dealArr:
        for cont in Acct1.UnConList:
            cont.OverDate(deal)                    
            
            if cont.TradeWay > 0:
                rTrend = 'UP'
            else:
                rTrend = 'DOWN'
            '''    
            if Cind.preKbadStop(vDeal = deal,vTrend = rTrend):
                cont.CloseContract(deal)            
                Acct1.AcctCloseCon()
                Acct1.totalAmt = Acct1.totalAmt - floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
                CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice,'Stop Loss':'Yes'})
                
                print 'Init Date: ' + date2str(cont.InitDate) + ' Init Price:' + str(cont.BuildPrice) +' stop price:' + str(cont.EvenPrice) +\
                ' stop loss at:' + date2str(deal.TradeDate) + ' TredeWay:' + str(cont.TradeWay)
            '''
            if cont.TradeWay > 0:
                if Cind.RsiStop(vDeal = deal,vTrend = rTrend,Criteria = upCriteria):
                    cont.CloseContract(deal)
                    Acct1.AcctCloseCon()
                    Acct1.totalAmt = Acct1.totalAmt + floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
                    CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice,'Stop Loss':'Yes'})
                    print 'Even Price:' + str(cont.EvenPrice) + ' End Date:' + str(cont.EndDate)
                    print 'Init Date: ' + date2str(cont.InitDate) + ' Init Price:' + str(cont.BuildPrice) +' stop price:' + str(cont.EvenPrice) +\
                    ' exit at:' + date2str(deal.TradeDate) + ' TredeWay:' + str(cont.TradeWay)
            else:
                if Cind.RsiStop(vDeal = deal,vTrend = rTrend,Criteria = downCriteria):
                    cont.CloseContract(deal)
                    Acct1.AcctCloseCon()
                    Acct1.totalAmt = Acct1.totalAmt + floatrou(((cont.EvenPrice * cont.Position * 0.003) + (cont.EvenPrice * cont.Position * 0.001425 * 0.6)))
                    CloseConArr.append({'InitDate':cont.InitDate,'EndDate':cont.EndDate,'DealAmt':cont.Position,'OpenPrice':cont.BuildPrice,'ClosePrice':cont.EvenPrice,'Stop Loss':'Yes'})
                    print 'Even Price:' + str(cont.EvenPrice) + ' End Date:' + str(cont.EndDate)
                    print 'Init Date: ' + date2str(cont.InitDate) + ' Init Price:' + str(cont.BuildPrice) +' stop price:' + str(cont.EvenPrice) +\
                    ' exit at:' + date2str(deal.TradeDate) + ' TredeWay:' + str(cont.TradeWay)
                
                
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
                    if (preDIp - preDIm) > 0:
                        #continue
                        #做空
                        cont1 = Contract(ContName=date2str(deal.TradeDate),Position = PostAmt*1000,vDateDeal = deal,TradeWay=-1)
                        Acct1.AddContr(cont1)
                        print 'preDIp:' + str(preDIp) + ' preDIm:' + str(preDIm) +' newDIp:' + str(newDIp)+ ' newDIm:' + str(newDIm)
                    else:
                        #做多
                        #continue
                        cont1 = Contract(ContName=date2str(deal.TradeDate),Position = PostAmt*1000,vDateDeal = deal,TradeWay=1)
                        Acct1.AddContr(cont1)
                        print 'preDIp:' + str(preDIp) + ' preDIm:' + str(preDIm) +' newDIp:' + str(newDIp)+ ' newDIm:' + str(newDIm) 
            
                    
    Acct_mkt_compare(RecDateArr,RecAmtArr,ClosePriceArr)   

                
            
DIProcess(vTarget='2207.TW')       
    
    
    