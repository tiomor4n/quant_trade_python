# -*- coding: utf-8 -*-
"""
figure_plot_output
Created on Sat Dec 19 09:57:21 2015

@author: simon
"""

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY,MonthLocator
from matplotlib.figure import Figure

from strategy1 import IndexCal
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import numpy as np
import matplotlib.ticker as mticker
from DataPipe import YahooFinance,TWNStockTIOMO,TWNFutureLocal
from ClsContract import DateDeal

def Acct_mkt_compare(x1,y1,y2):
    dtloc = mdates.DayLocator()
    weekloc = mdates.WeekdayLocator()
    mloc = mdates.MonthLocator(interval=3)
    dtFmt = mdates.DateFormatter('%Y/%m')
    
    fig ,ax= plt.subplots()
    '''
    這邊要把最外面的0~1的邊界x軸值拿掉
    '''
    ax.axison=False
    ax = fig.add_subplot(111)
    par1 = ax.twinx()
    ax.plot(x1,y1,color = 'red')
    par1.plot(x1,y2,color='blue')
    
    ax.xaxis.set_major_locator(mloc)
    ax.xaxis.set_major_formatter(dtFmt)
    ax.xaxis.set_minor_locator(weekloc)
    ax.axison=True
    ax.grid(True)
    ax.set_xlim(x1[0], x1[-1])
    fig.autofmt_xdate()    
    plt.savefig(u"test.png", dpi=100, format="png")    
    plt.show()
    
def Acct_mkt_candle(dealArr = [],AcctAmtArr=[]):
    from matplotlib.finance import candlestick_ohlc
    datenumArr = []
    openp = []
    highp = []
    lowp=[]
    closep=[]
    volume=[]
    
    for a in dealArr:
        datenumArr.append(mdates.date2num(a.TradeDate))
        openp.append(a.OpenPrice)
        highp.append(a.HighPrice)
        lowp.append(a.LowPrice)
        closep.append(a.ClosePrice)
        volume.append(a.DealAmt)
        x = 0
        y = len(datenumArr)
        
    newAr = []
    while x < y:
        appendLine = datenumArr[x],openp[x],highp[x],lowp[x],closep[x],volume[x]
        newAr.append(appendLine)
        x+=1
        
        
    fig = plt.figure(facecolor='#07000d')
    ax1 = plt.subplot2grid((3,2), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
    fig.set_size_inches(18.5, 10.5)
    candlestick_ohlc(ax1,newAr[:],width=.6,colorup='#ff1717',colordown='#53c156')
    par1 = ax1.twinx()    
    par1.plot(datenumArr[:],AcctAmtArr[:],color = "red",linewidth=1)    
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    par1.yaxis.label.set_color("w")
    par1.spines['right'].set_color("#5998ff")
    par1.spines['bottom'].set_color("#5998ff")
    par1.spines['top'].set_color("#5998ff")
    par1.spines['left'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    par1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    #plt.ylabel('Stock price and Volume')
    plt.savefig(u"test.png", format="png")
    plt.show()
    
