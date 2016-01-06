# -*- coding: utf-8 -*-
import BaseFunction
from ClsContract import DateDeal
from BaseFunction import date2str
from BaseFunction import str2date
import numpy as np
import math
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import datetime
import sys


class durationMax(object):
    def __init__(self,vdealarr = []):  
        self.dealarr = vdealarr
        
        self.dateArr = []
        self.OpenPriceArr = []
        self.HighPriceArr = []
        self.LowPriceArr = []
        self.ClosePriceArr = []
        
        for deal in self.dealarr:
            self.dateArr.append(deal.TradeDate)
            self.OpenPriceArr.append(deal.OpenPrice)
            self.HighPriceArr.append(deal.HighPrice)
            self.LowPriceArr.append(deal.LowPrice)
            self.ClosePriceArr.append(deal.ClosePrice)
            
    
    '''
    給定一個時間值(TargetDate)，計算該時間值最新進來的ClosePrice
    是否為包含此時間之duration內的最大值
    '''    
    def CalMax(self,vTargetDate='',Period=20):
        if(vTargetDate == ''):
            return False
        else:
            if(self.dateArr.index(str2date(vTargetDate))<(Period-1)):
                return False
            else:
                T=self.dateArr.index(str2date(vTargetDate))
                latestP = self.ClosePriceArr[T]
                pArr = self.ClosePriceArr[T-(Period-1):T+1]
                if (latestP == max(pArr)):
                    return True
                else:
                    return False
                    

class IndexCal(object):
    def __init__(self,vdealarr=[]):
        self.dealarr = vdealarr
        self.dateArr = []
        self.OpenPriceArr = []
        self.HighPriceArr = []
        self.LowPriceArr = []
        self.ClosePriceArr = []
        for deal in self.dealarr:
            self.dateArr.append(deal.TradeDate)
            self.OpenPriceArr.append(deal.OpenPrice)
            self.HighPriceArr.append(deal.HighPrice)
            self.LowPriceArr.append(deal.LowPrice)
            self.ClosePriceArr.append(deal.ClosePrice)
            
    

    def moving_average(self,x, n, vtype='simple'):
        x = np.asarray(x)
        if vtype=='simple':
            weights = np.ones(n)
        else:
            weights = np.exp(np.linspace(-1., 0., n))

        weights /= weights.sum()

        a =  np.convolve(x, weights, mode='full')[:len(x)]
        a[:n-1] = None
        return a
            
    '''
    計算該區間的給訂日期後ATR
    '''        
    def ATRCal(self,vRange=20):
        ATRArr = []
        TRArr = []    
        preprice = 0.0
        for deal in self.dealarr:
            if self.dealarr.index(deal) == 0:
                TRArr.append(deal.HighPrice - deal.LowPrice)
                #print len(TRArr)
            else:
                TRArr.append(max(deal.HighPrice-deal.LowPrice,math.fabs(deal.HighPrice - preprice),math.fabs(preprice - deal.LowPrice)))
                
            preprice = deal.ClosePrice
            
        firstATR = np.mean(TRArr[:vRange])
        ATRArr.append(firstATR)
        
        for TR in TRArr[vRange:]:
            if len(ATRArr) == 1:
                ATRArr.append((firstATR * (vRange-1) + TR)/vRange)
            else:
                ATRArr.append((ATRArr[-1] * (vRange-1) + TR)/vRange)
            
        return ATRArr,self.dateArr[vRange:]
        
    
    def MACal(self, vRange1=20,vRange2=40):            
        def add_field(a, descr):    
            if a.dtype.fields is None:
                raise ValueError, "'A' must be a structured numpy array"
            b = np.empty(a.shape, dtype=a.dtype.descr + descr)
            for name in a.dtype.names:
                b[name] = a[name]
            return b
        
        ma1 = self.moving_average(self.ClosePriceArr,vRange1)
        ma2 = self.moving_average(self.ClosePriceArr,vRange2)
    
        axx = np.zeros(len(self.dateArr))
        ax1 = np.array(axx,dtype = [('date','O')])
        i=0
        for dt in self.dateArr:
            ax1['date'][i]=dt
            i+=1
   
        ax2 = add_field(ax1,[('close','f8')])        
        i=0
        for item in self.ClosePriceArr:
            ax2['close'][i] = item
            i+=1
        
        ax3 = add_field(ax2,[('ma1','f8')])
        i=0
        for item in ma1:
            ax3['ma1'][i] = item
            i+=1
             
        ax4 = add_field(ax3,[('ma2','f8')])
        i=0
        for item in ma2:
            ax4['ma2'][i] = item
            i+=1
            
        return ax4
        
    def MAPosition(self,vRange=0,vDeal=DateDeal,vLocate='UP'):
        if vRange > len(self.dealarr):
            print 'MA range < dealArr'
            sys.exit()
        MAArr = []    
        
        MAArr = self.moving_average(x=self.ClosePriceArr,n=vRange)    
        MAValue = MAArr[self.dateArr.index(vDeal.TradeDate)]
        #print str(vDeal.ClosePrice) + ',' + str(MAValue)
        if vLocate == 'UP':
            return vDeal.ClosePrice > MAValue
        else:
            return vDeal.ClosePrice < MAValue
                
          
    
            
    def WindowTrend(self,vLen = 11,vDeal = DateDeal,vTrend = 'UP'):
        if len(self.dealarr) < vLen:
            print str(len(self.dealarr))
            print str(vLen)
            print 'dealArr < window'
            sys.exit()
        ind = self.dateArr.index(vDeal.TradeDate)
        if ind < vLen:
            return None
        windowstart = ind - vLen
        windowend = ind
        window = self.dealarr[windowstart:windowend]
        close0 = window[0].ClosePrice
        close1 = window[2].ClosePrice
        close2 = window[4].ClosePrice
        close3 = window[6].ClosePrice
        close4 = window[8].ClosePrice
        close5 = window[10].ClosePrice
        preclose = [close0,close1,close2,close3]
        nextclose = [close4,close5]
        if vTrend == 'UP':
            return close5 > close4 * 1.1 and np.mean(nextclose) > 1.3 * (np.mean(preclose))
        else:
            return close5 * 1.1 < close4 and np.mean(nextclose) * 1.3 < (np.mean(preclose))
            
    def CalADX(self,vDeal = DateDeal):
        ind = self.dateArr.index(vDeal.TradeDate)
        window = self.dealarr[ind-1:ind]
        
            
        
    def preLowStop(self,vDeal = DateDeal,vTrend = 'UP'):
        def preHighLow(self,vDateDeal):
            ind = self.dateArr.index(vDeal.TradeDate)
            PreHigh = self.dealarr[ind-1].HighPrice
            PreLow = self.dealarr[ind-1].LowPrice
            return PreHigh,PreLow
        
        rPreHigh,rPreLow =   preHighLow(vDeal)      
        if vTrend == 'UP':
            return vDeal.ClosePrice < rPreLow
        else:
            return vDeal.ClosePrice > rPreHigh
    
    def ERatioCal(self,vRange=50):
        ERatioArr = []
        ATRArr = ATRCal(vRange)
        ERatio=0.0
        orig = 0.0
        MFE = 0.0
        MAE = 0.0
        MFEArr=[]
        MAEArr=[]
        
        
        for deal in self.dealarr:
            orig = deal.ClosePrice
            MFE = max(self.ClosePriceArr[self.dealarr.index(deal):self.dealarr.index(deal)+vRange]) - orig
            MAE = orig - min(self.ClosePriceArr[self.dealarr.index(deal):self.dealarr.index(deal)+vRange])
            MFEArr.append(MFE)
            MAEArr.append(MAE)
        
        
        
        
        

    


                 
        
        
            
        
        