# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 21:19:43 2015

@author: simon
"""
import os

import datetime
import matplotlib.dates as mdates

def str2date(vdate,vformat='%Y/%m/%d'):
    return datetime.datetime.strptime(vdate,vformat)
        
def date2str(vdate,vformat = '%Y/%m/%d'):
    return datetime.datetime.strftime(vdate,vformat)
    
    
def modStr2Num(vdate,vFORMAT='%Y%m%d'):
    return mdates.date2num(datetime.datetime.strptime(vdate,vFORMAT))
    

def floatrou(vfloat,vdigit=2):
    return round(float(vfloat),vdigit)
    
def txtpercent(vfloat,vdigit=4):
    return "{}%".format(str(round(float(vfloat),vdigit) * 100))
    

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
 
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
     
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False    

            
def writetxt(vfilename= '',vstr=''):
    if os.path.isfile(vfilename):
        f= open(vfilename,'a')
    else:
        f= open(vfilename,'w')
        
    f.write(vstr + '\n')  
    f.close()
    
    
    