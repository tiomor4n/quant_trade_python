# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:37:04 2016

@author: simon
"""

def DIProcess():
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
    from DataPipe import YahooFinance
    from figure_plot_output import Acct_mkt_compare
    from ClsGenReport import CalCAGR,CalSharpInd,CalDD,BackwardTest
    
    dealArr = YahooFinance()
    Cind = IndexCal(dealArr)
    '''
    用DI+ > DI-做多，DI- <DI+做空，用prebadK停損
    '''
    lenw = 14
    i = 0
    preDIp = -1
    preDIm = -1
    newDIp = -1
    newDIm = -1
    #因為不會有負值，用-1當作初始值
    for deal in dealArr:
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
                        #做空
                    else:
                        #做多
                
            
        
    
    
    