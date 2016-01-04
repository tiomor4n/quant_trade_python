# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 08:04:52 2015
ClassName:ClsGenReport
@author: simon
"""

import numpy as np
import math
import sys


def CalpertotalAmtArr(vtotalAmtArr = []):
    result = []
    for i in range(len(vtotalAmtArr)):
        if i == 0: 
            continue
        else:
            result.append(float(vtotalAmtArr[i]) - float(vtotalAmtArr[0]) / float(vtotalAmtArr[0]))
    return result

def CalCAGR(vtotalAmtArr=[]):
    CAGR = 0.0
    CAGR = (float(vtotalAmtArr[-1]) - float(vtotalAmtArr[0])) / float(vtotalAmtArr[0])
    return CAGR
    
def CalSharpInd(vtotalAmtArr=[],Rf = 1.3):
    Rp = 0.0
    Rp = float(CalCAGR(vtotalAmtArr))
    #print 'Rp:' + str(Rp)
    return (Rp - Rf) / math.sqrt(np.var(CalpertotalAmtArr(vtotalAmtArr)))
           
def CalDD(vtotalAmtArr=[]):
    maxDDCnt = 0    
    DDCnt = 0
    maxDDAmt = 0.
    DDArr = []
    C = vtotalAmtArr[0]
    for ax in vtotalAmtArr[1:]:
        C = max(ax,C)
        if C == ax:
            DDArr.append(0)
            DDCnt = 0
        else:
            DDArr.append(float(ax - C)/float(C))
            DDCnt = DDCnt + 1
            maxDDCnt = max(maxDDCnt,DDCnt)
    maxDDAmt = min(DDArr)
    return maxDDAmt,maxDDCnt
            
            
    
def genPDFRpt():
    from reportlab.pdfgen import canvas 
    y = [2,2,5,16,15,14,13,12,11,11,11,10,8,9,4,6,4,2,-3] 
    p=canvas.Canvas('Hello_world.pdf')
    for a in y:
        p.drawString(100,100,str(a) + '\n')
    p.showPage()  
    p.save()  


def hello(c):
    from PIL import Image
    from reportlab.lib.units import inch
    # move the origin up and to the left
    for i in range(5):
        c.drawString(100,100+10*i,"Hello World " + str(i))
    c.drawImage('aa.png',1,150)
    c.showPage()
    c.save()

'''
y = [2,2,5,16,15,14,13,12,11,11,11,10,8,9,4,6,4,2,-3]   
print 'CAGR:' + str(CalCAGR(y)) 
print 'SHARP:' + str(CalSharpInd(y))
print 'DD:' + str(CalDD(y))
print 'DDAmt:' + str(CalDDAmt(y))
'''

def BackwardTest(vImage,IndexArr):
    from reportlab.pdfgen import canvas
    c = canvas.Canvas("BackwardTest.pdf",bottomup=1)
    if len(IndexArr) == 0:
        c.drawString(100,100+10,"no Index")
        sys.exit()
    i = 1    
    for txt in IndexArr:
        c.drawString(100,100+10*i, txt)
        i=i+1
    c.drawImage('test.png',1,150)
    c.showPage()
    c.save()
    
        


'''
from reportlab.pdfgen import canvas
c = canvas.Canvas("hello.pdf",bottomup=1)
hello(c)
ax = ['A','B','C','D']
BackwardTest(vImage = None,IndexArr = ax)
'''
