# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 09:57:21 2015

@author: simon
"""

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY,MonthLocator
from matplotlib.figure import Figure

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
