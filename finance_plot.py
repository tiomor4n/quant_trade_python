# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:45:12 2015

@author: simon
"""

import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


def moving_average(x, n, type='simple'):
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type=='simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()


    a =  np.convolve(x, weights, mode='full')[:len(x)]
    a[:n-1] = a[n-1]
    return a
'''
#卷積範例
#np.convolve([1,2,3,4,5],[0.25,0.25,0.25,0.25])
'''



def relative_strength(prices, n=14):
    deltas = np.diff(prices)
    '''
    後一個值減去前一個值的陣列
    '''
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    '''
    做出跟prices一樣多的0陣列
    '''
    #前14個
    rsi[:n] = 100. - 100./(1.+rs)
    '''
    計算rsi的關鍵式子
    移項計算後會等於rsi的計算公式
    (u/(u+d)) * 100
    u = 一段期間內上漲值/期間長度
    d = 一段期間內下跌值/期間長度
    '''    
    
    
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
    


startdate = datetime.date(2015,9,10)
today = enddate = datetime.date.today()
ticker = 'SPY'


fh = finance.fetch_historical_yahoo(ticker, startdate, enddate)
r = mlab.csv2rec(fh)
fh.close()
r.sort()

prices = r.close

ma20 = moving_average(prices, 20, type='simple')

