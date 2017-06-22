#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 10:10:57 2017
@author: @author: Murex Integration 2017
"""

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
	except:
		print "something wrong with the maturity conversion"