# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 21:42:32 2015

@author: simon
"""

class DateDeal(object):
    def __init__(self, TradeDate='',DealAmt=0,OpenPrice=0.0,HighPrice=0.0,LowPrice=0.0,ClosePrice=0.0):
        self.TradeDate = TradeDate
        self.OpenPrice= OpenPrice
        self.HighPrice=HighPrice
        self.LowPrice=LowPrice
        self.ClosePrice=ClosePrice
        self.DealAmt=DealAmt
        
class FutDateDeal(DateDeal):
    def __init__(self, TradeDate='',ContDate='',DealAmt=0,OpenPrice=0.0,HighPrice=0.0,LowPrice=0.0,ClosePrice=0.0,NotEvenAmt=0):
        self.TradeDate = TradeDate
        self.OpenPrice= OpenPrice
        self.HighPrice=HighPrice
        self.LowPrice=LowPrice
        self.ClosePrice=ClosePrice
        self.DealAmt=DealAmt
        self.ContDate = ContDate
        self.NotEvenAmt = NotEvenAmt

    
class Contract(object):
    def __init__(self,ContName='',BuildPrice = 0.,Position=0,TradeWay=1,vDateDeal=DateDeal,\
    EvenPrice=0.0,dicRecord={},OpenApp='Close',vStopLoss = 'None'):
        self.ContName = ContName
        self.InitDate = vDateDeal.TradeDate
        self.EndDate = ''
        if OpenApp == 'Close':
            self.BuildPrice = vDateDeal.ClosePrice
        elif OpenApp == 'Open':
            self.BuildPrice = vDateDeal.OpenPrice
        elif OpenApp == 'Assign':
            self.BuildPrice = BuildPrice
        self.unEvenPrice = vDateDeal.ClosePrice
        self.unGainLoss = (vDateDeal.ClosePrice-BuildPrice) * Position * TradeWay
        self.Position = Position
        self.TradeWay = TradeWay
        self.EvenPrice = 0.0
        self.GainLoss = 0.0
        self.dicRecord = {}
        self.HoldDuration=1
        self.pre_unGainLoss = 0.0
        


    def OverDate(self,vDateDeal=DateDeal):
        self.vDateDeal = vDateDeal
        self.unEvenPrice=vDateDeal.ClosePrice        
        self.unGainLoss=(vDateDeal.ClosePrice-self.BuildPrice) * self.Position * self.TradeWay
        self.pre_unGainLoss = max(self.pre_unGainLoss,self.unGainLoss)
        self.HoldDuration += 1

    

    def CloseContract(self,vDateDeal=DateDeal,ClosePrice=0.0,CloseApp = 'Close'):
        self.EndDate = vDateDeal.TradeDate
        if CloseApp == 'Close':
            self.EvenPrice = vDateDeal.ClosePrice
        elif CloseApp == 'Open':
            self.EvenPrice = vDateDeal.OpenPrice
        elif CloseApp == 'Assign':
            self.EvenPrice = ClosePrice
        self.GainLoss = (self.EvenPrice-self.BuildPrice) * self.Position * self.TradeWay
        
    def Net_Trailling(self,N = 10000,ratio=0.5):
        return self.pre_unGainLoss > N and self.unGainLoss < self.pre_unGainLoss * ratio
        
    def StopLoss_FixPrice(self,N):
        return (self.unEvenPrice - self.BuildPrice ) * self.TradeWay > N
        
        

        
        
class Account(object):
    def __init__(self,ConList = [],initAmt=0,initDate = '',TradeDate = '',dicRecord = {}):
        self.initDate = initDate
        self.TradeDate  = TradeDate
        self.initAmt = initAmt
        self.ConList = ConList
        self.totalAmt = initAmt
        self.dicRecord = {}
        self.UnConList=[]
        self.ConList = ConList

    def AddContr(self,vContract=Contract):
        self.UnConList.append(vContract)

    def CalUnPL(self):
        total = self.totalAmt
        for tr in self.UnConList:
            if tr.EndDate == '':
                total = total + tr.unGainLoss
        self.totalAmt= total
        
    def AcctCloseCon(self):
        for tr in self.UnConList:
            if tr.EndDate != '':
                self.UnConList.remove(tr)
                self.ConList.append(tr)
                self.totalAmt = self.totalAmt + tr.GainLoss
                
     
        
        
        