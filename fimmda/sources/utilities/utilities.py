#!/usr/bin/env python
"""
Title                                       :utilities.py
Description                        :This module defines the utility functions used by the tool
Author                                  :DANG Steve
Python_version                :2.7
-------------------------------
Change log:
Version                                Date                                      Who                                      Description
v1.0                                        20170822                             Steve                                    1st release
v1.1                                        20170919                             Steve                                    add getDate() function

"""
################################################################
import logging, sys, os
#from utilities.TransformationException import * 

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
################################################################
#get date from a file name
# for example FIMMDA_PARYIELD_DAILY_20170902.csv into 20170902 
def getDateFromFileName(str2):
    try:
        main_file = str2.split(".csv")[0]
        #get the main file name FIMMDA_PARYIELD_DAILY_20170902
        temp_str = main_file.split("_")
        #return the last part 20170902
        return temp_str[-1]
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.debug("{} {} {} {}".format(exc_type, fname, exc_tb.tb_lineno, e.message))
        raise TransformationException(ERROR_106+" : "+str2)
