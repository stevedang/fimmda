#!/usr/bin/env python
"""
Murex Integration 2017
----------------------
Change log:
20170822: 1st release
"""
################################################################
import logging, sys, os
from mapping.TransformationException import * 

#define the log
log = logging.getLogger(__name__)

################################################################
#check if a variable is a number
def isNumber(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True
################################################################
# get maturity from a string
# translates the maturity from figures 0.5, 1.5, 2.5 to 6M, 18M, 24M    
# and 1.0, 2.0 etc to 1Y, 2Y
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
		# if there is an error throw error code 105 to the outer function
        raise TransformationException(ERROR_105+" maturity: "+str2)