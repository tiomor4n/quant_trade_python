# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 23:48:24 2016

@author: simon
"""
from strategy1 import IndexCal
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import numpy as np
import matplotlib.ticker as mticker
from DataPipe import YahooFinance,TWNStockTIOMO,TWNFutureLocal

def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    """
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    """
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow
    
def graphData(stock,MA1,MA2):
    '''
        Use this to dynamically pull a stock:
    '''    
    dealArr = YahooFinance(vTarget = stock)
    Cind = IndexCal(dealArr)
    datenumArr = []
    openp = []
    highp = []
    lowp=[]
    closep=[]
    volume=[]
    DIpArr = []
    DImArr = []
    for a in Cind.dealarr:
        datenumArr.append(mdates.date2num(a.TradeDate))
        openp.append(a.OpenPrice)
        highp.append(a.HighPrice)
        lowp.append(a.LowPrice)
        closep.append(a.ClosePrice)
        volume.append(a.DealAmt)
        DIp,DIm = Cind.DICal(a)
        if DIp != 0:
            DIpArr.append(DIp)
            DImArr.append(DIm)
                
    x = 0
    y = len(datenumArr)
    newAr = []
    while x < y:
        appendLine = datenumArr[x],openp[x],highp[x],lowp[x],closep[x],volume[x]
        newAr.append(appendLine)
        x+=1
    
    '''
    處理要加在K線圖的其他指標
    '''
    Av1 = movingaverage(closep, MA1)
    Av2 = movingaverage(closep, MA2)
    
    SP = len(datenumArr[MA2-1:])
        
    fig = plt.figure(facecolor='#07000d')

    ax1 = plt.subplot2grid((3,2), (1,0), rowspan=4, colspan=4, axisbg='#07000d')
    fig.set_size_inches(18.5, 10.5)
    candlestick_ohlc(ax1, newAr[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
    
    par1 = ax1.twinx()

    Label1 = str(MA1)+' SMA'
    Label2 = str(MA2)+' SMA'

    ax1.plot(datenumArr[-SP:],Av1[-SP:],'#e1edf9',label=Label1, linewidth=1.5)
    ax1.plot(datenumArr[-SP:],Av2[-SP:],'#4ee6fd',label=Label2, linewidth=1.5)
    #par1.plot(datenumArr[-SP:],randarr[-SP:],color = "red",linewidth=1)
    par1.plot(datenumArr[-SP:],DIpArr[-SP:],color = "red",linewidth=1)
    par1.plot(datenumArr[-SP:],DImArr[-SP:],color = "blue",linewidth=1)
    
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    par1.yaxis.label.set_color("w")
    par1.spines['right'].set_color("#5998ff")
    par1.spines['bottom'].set_color("#5998ff")
    par1.spines['top'].set_color("#5998ff")
    par1.spines['left'].set_color("#5998ff")
    #ax1.fill_between(datenumArr[-SP:],DIpArr[-SP:],50,where=(DIpArr[-SP:]>=50),facecolor='blue',edgecolor='blue',alpha=0.5)
    
    ax1.tick_params(axis='y', colors='w')
    par1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.savefig(u"test.png", dpi=100, format="png")  
    #except Exception,e:
    #    print str(e), 'failed to pull pricing data'
    
    ax0 = plt.subplot2grid((6,4), (0,0), sharex=ax1, rowspan=2, colspan=4, axisbg='#07000d')
    rsi = rsiFunc(closep)
    rsiCol = '#c1f9f7'
    posCol = '#386d13'
    negCol = '#8f2020'
    ax0.plot(datenumArr[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
    ax0.axhline(70, color=negCol)
    ax0.axhline(30, color=posCol)
    ax0.fill_between(datenumArr[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
    ax0.fill_between(datenumArr[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
    ax0.set_yticks([30,70])
    ax0.yaxis.label.set_color("w")
    ax0.spines['bottom'].set_color("#5998ff")
    ax0.spines['top'].set_color("#5998ff")
    ax0.spines['left'].set_color("#5998ff")
    ax0.spines['right'].set_color("#5998ff")
    ax0.tick_params(axis='y', colors='w')
    ax0.tick_params(axis='x', colors='w')
    plt.ylabel('RSI')
    
    plt.suptitle(stock.upper(),color='w')
        
graphData('2891.TW',10,50)