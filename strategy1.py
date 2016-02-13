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
        self.DealAmtArr = []
        for deal in self.dealarr:
            self.dateArr.append(deal.TradeDate)
            self.OpenPriceArr.append(deal.OpenPrice)
            self.HighPriceArr.append(deal.HighPrice)
            self.LowPriceArr.append(deal.LowPrice)
            self.ClosePriceArr.append(deal.ClosePrice)
            self.DealAmtArr.append(deal.DealAmt)
            
    

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
            
    def Oscillator(self,vDeal=DateDeal):
        ind = self.dateArr.index(vDeal.TradeDate)
        
            
    def CalADX(self,vDeal = DateDeal):
        ind = self.dateArr.index(vDeal.TradeDate)
        window = self.dealarr[ind-1:ind]
        TRArr = []    
        preprice = 0.0
        for deal in self.dealarr:
            if self.dealarr.index(deal) == 0:
                TRArr.append(deal.HighPrice - deal.LowPrice)
                #print len(TRArr)
            else:
                TRArr.append(max(deal.HighPrice-deal.LowPrice,math.fabs(deal.HighPrice - preprice),math.fabs(preprice - deal.LowPrice)))
                
            preprice = deal.ClosePrice
            
        
        
    def preHighLow(self,vDateDeal,vintWindow):
        ind = self.dateArr.index(vDateDeal.TradeDate)
        window = self.dealarr[ind-vintWindow:ind]
        higharr = []
        lowarr = []
        for ar in window:
            higharr.append(ar.HighPrice)
            lowarr.append(ar.LowPrice)
        PreHigh = max(higharr)
        PreLow = min(lowarr)
        return PreHigh,PreLow         
        
    def preLowStop(self,vDeal = DateDeal,vintWindow = 3,vTrend = 'UP'):
        rPreHigh,rPreLow =  self.preHighLow(vDateDeal = vDeal,vintWindow = vintWindow)      
        if vTrend == 'UP':
            return vDeal.ClosePrice < rPreLow
        else:
            return vDeal.ClosePrice > rPreHigh
 
    '''
    已進場當根K bar與前一根Kbar最低點比較，誰的低點低誰當第一個停損
    接下來只要K br創新高，就已創新高的K bar的低點當停損點
    介面:
    input:datedeal,是否為第一個，運算前停損價，運算前最高價,vTrend
    output:運算後停損價，運算後最高價，是否停損
    
    '''
    def preKbadStop(self,vDeal = DateDeal,visFirst = False,vprebadp=0,vpregoodp=0,vTrend = 'UP'):
        ind = self.dateArr.index(vDeal.TradeDate)
        if vTrend == 'UP':
            if visFirst == True:
                goodp = vDeal.HighPrice                
                badp = min(self.dealarr[ind].LowPrice,self.dealarr[ind-1].LowPrice)
                StopL = False
                return badp,goodp,StopL
            else:
                goodp = max(vDeal.HighPrice,vpregoodp)
                if goodp == vDeal.HighPrice:
                    badp = vDeal.LowPrice
                else:
                    badp = vprebadp
                StopL = vDeal.ClosePrice < vprebadp                
                return badp,goodp,StopL
        else:
            if visFirst == True:
                goodp = vDeal.LowPrice                
                badp = min(self.dealarr[ind].HighPrice,self.dealarr[ind-1].HighPrice)
                StopL = False
                return badp,goodp,StopL
            else:
                goodp = min(vDeal.LowPrice,vpregoodp)
                if goodp == vDeal.LowPrice:
                    badp = vDeal.HighPrice
                else:
                    badp = vprebadp
                StopL = vDeal.ClosePrice > vprebadp                
                return badp,goodp,StopL
         
    '''
    def preKbadStop(self,vDeal = DateDeal,vTrend = 'UP'):
        def preKbadArrCal(self,vDeal = DateDeal,vTrend):
            preKbadArr = []
            ind = self.dateArr.index(vDeal.TradeDate)
            if vTrend == 'UP':
                badp = min(self.dealarr[ind].LowPrice,self.dealarr[ind-1].LowPrice)
                preKbadArr.append(badp)
                bestp = vDeal.HighPrice
                for deal in self.dealarr[ind+1:]:
                    bestp = max(deal.HighPrice,bestp)
                    if deal.HighPrice == bestp:
                        badp = min(badp,deal.LowPrice)
                    preKbadArr.append(badp)
            else:
                badp = max(self.dealarr[ind].HighPrice,self.dealarr[ind-1].HighPrice)
                preKbadArr.append(badp)
                bestp = vDeal.LowPrice
                for deal in self.dealarr[ind+1:]:
                    bestp = max(deal.LowPrice,bestp)
                    if deal.LowPrice == bestp:
                        badp = min(badp,deal.HighPrice)
                    preKbadArr.append(badp)
            return preKbadArr
    '''           
    
    '''
    TR計算
    如是第一個TR = Hight - Lowt
    如否，TR = max(Hight - Lowt,Higtt - CloseT-1,CloseT-1 -Lowt)
    '''                    
    def TRCal(self,vDeal = DateDeal,visFirst = False):
        rTR=0
        if visFirst:
            rTR = vDeal.HighPrice - vDeal.LowPrice
        else:
            ind = self.dateArr.index(vDeal.TradeDate)
            preDeal = self.dealarr[ind-1]
            rTR = max(vDeal.HighPrice - vDeal.LowPrice,vDeal.HighPrice - preDeal.ClosePrice,preDeal.ClosePrice - vDeal.LowPrice)
        return rTR
        
    def DICal(self,vDeal = DateDeal,vwindow = 14,visFirst = False,vpreDM = 0):
        ind = self.dateArr.index(vDeal.TradeDate)
        if len(self.dealarr[0:ind])< vwindow:
            #print "transaction date should longer then window"
            #sys.exit()
            return 0,0
        #windowArr = self.dealarr[ind-vwindow+1:ind+1]   #這樣會抓最後一個為vDeal的vwindow個元素陣列  要多抓一個才能算TR DM
        windowArr = self.dealarr[ind-vwindow:ind+1]   #這樣會抓最後一個為vDeal的vwindow個元素陣列  要多抓一個才能算TR DM
        DMplus = 0
        DMminus = 0
        rTR = 0
        i = 0
        for i in range(vwindow+1):
            if i == 0:
                continue
            else:
                DMplus += max(0,windowArr[i].HighPrice - windowArr[i-1].HighPrice)
                DMminus += max(0,windowArr[i-1].LowPrice - windowArr[i].LowPrice)
                rTR += self.TRCal(windowArr[i])
        
        DIplus = (DMplus/rTR) * 100
        DIminus = (DMminus/rTR) * 100
        
        return DIplus,DIminus
    
    def RsiCal(self,vwindow):
        prices = self.ClosePriceArr
        deltas = np.diff(prices)
        seed = deltas[:vwindow+1]
        up = seed[seed>=0].sum()/vwindow
        down = -seed[seed<0].sum()/vwindow
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:vwindow] = 100. - 100./(1.+rs)
    
        for i in range(vwindow, len(prices)):
            delta = deltas[i-1] # cause the diff is 1 shorter
    
            if delta>0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
    
            up = (up*(vwindow-1) + upval)/vwindow
            down = (down*(vwindow-1) + downval)/vwindow
    
            rs = up/down
            rsi[i] = 100. - 100./(1.+rs)
    
        return rsi
        '''
        ind = self.dateArr.index(vDeal.TradeDate)
        if len(self.dealarr[0:ind])<vwindow:
            return 0
        
        windowArr = self.ClosePriceArr[ind-vwindow:ind+1] 
        diffw = np.diff(windowArr)
        up = diffw[diffw>0].sum()/vwindow
        down = -diffw[diffw<0].sum()/vwindow
        rs = up/down
        rsi = 100. - 100./(1.+rs)
        return rsi
        '''
        
    def RsiStop(self,vTrend,Criteria,vwindow,vRsiArr=[],vDeal = DateDeal):
        #RsiArr = self.RsiCal(vwindow = vwindow)
        RsiArr = vRsiArr
        ind = self.dateArr.index(vDeal.TradeDate)
        if ind < vwindow + 1:
            print 'error tradedate'
            sys.exit()
        preRsi = RsiArr[ind-1]
        nowRsi = RsiArr[ind]
        if vTrend == 'UP':
            return nowRsi < Criteria <= preRsi 
        else:    
            return preRsi <= Criteria < nowRsi
        
         

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
       