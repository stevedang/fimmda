#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 10:10:57 2017
@author: @author: Murex Integration 2017
"""
import logging, sys, os
from mapping.fimmdaException import * 

#define the log
log = logging.getLogger(__name__)

def isNumber(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True
    
def getMaturity(str2):
    if not isNumber(str2):
        return str2
    maturity = ""
    try:
        temp = float(str2);
        if temp.is_integer():
            maturity = str(int(temp)) + "Y"
        else:
            maturity = str(int(temp * 12)) + "M"
        return maturity;
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.debug("{} {} {} {}".format(exc_type, fname, exc_tb.tb_lineno, e.message))
        raise FimmdaException(ERROR_105+" maturity: "+str2)