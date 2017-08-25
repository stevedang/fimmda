#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Murex Integration 2017
----------------------
Change log:
20170822: 1st release
"""
##########################################
#from  utilities import *
import os, csv, re, sys, os, argparse, logging
import ConfigParser
from utilities import utilities
from utilities.TransformationException import *

#define the log
log = logging.getLogger(__name__)

config = ConfigParser.ConfigParser()

#==============================================================================
# Main configuration from properties.ini
config.read("sources/config/properties.ini")
demiliter= config.get("General","demiliter")
input_folder = config.get("General","input_folder")
output_folder = config.get("General","output_folder")
#==============================================================================
#Mapping 
config.read("sources/mapping/mapping.ini")
table_name_list = [
                   ["PSU & Fis", "PSU"],
                   ["NBFCs","NBFC"],
                   ["CORPORATES","CORP"],
                   ["PSL PTC spread","PSL"],
                   ["SG","SDL"],
                   ["UDAY/Discom","UDAY"],
                   ["AT1","AT1"]                   
                   ]
rating_label_list = config.get("ZERO_SPREAD","rating_label_list").split(",")
#rating_label_list = ["AAA","AA+","AA","AA-","A+","A","A-","BBB+","BBB","BBB-","BB+","BB","Unrated"]
csv_header = config.get("PAR_SPREAD","csv_header")
output_file = config.get("PAR_SPREAD","output_file")
input_file = ""
row_format_reg = config.get("PAR_SPREAD","row_format_reg")
header_row = config.get("PAR_SPREAD","header_row").split(",")
fixed_data = config.get("PAR_SPREAD","fixed_data").split(",")
starting_row = config.get("PAR_SPREAD","starting_row")
testing = config.get("PAR_SPREAD","testing")
bdcs_type = config.get("PAR_SPREAD","bdcs_type").split(",")
#==============================================================================
class Table:
    def __init__(self):
        self.name = ""
        self.maturityList = []
        self.ratingList = []
        #declare a 2 dimension arrays to hold the data
        self.dataNodeList = []

    def addName(self,name): 
        for i in table_name_list:
            if i[0] in name:
                self.name = i[1]
                break
            
    def addMaturityList(self,list2): # add the annualised into the maturity list
        for i in list2: 
            if utilities.isNumber(i): 
                log.debug("addMaturityList {}".format(i))
                self.maturityList.append(utilities.getMaturity(i))
            #self.maturityList.append(utilities.getMaturity(i))
            
    def addRating(self,str2):
        found = False
        #cross check with the valid list
        for i in rating_label_list:
            log.debug("i = {}, str2 = {}".format(i,str2))
            if i == str2:               
                #add AAA, AAA+, AAA- ,etc. into the list
                #append the name, such as PSU AAA
                log.debug("adding rating into the list {}".format(self.name + " "+ str2))
                self.ratingList.append(self.name + " "+ str2) 
                found = True
                break
        if not found:
            self.ratingList.append(self.name ) #otherwise it will be just name such as SDP
    
    def addDataList(self,newlist):
        self.dataNodeList.append(newlist)
    def getName(self): 
        return self.name
    def getDataList(self): return self.dataNodeList        
    def getMaturityList(self): return self.maturityList
    def getRatingList(self): return self.ratingList
#==============================================================================

def main(args):
    input_file = args
    source_file = input_folder + input_file    
    log.info("Reading Zero Spread input file {} ".format(source_file))
    tableList = []
    # open csv file
    try:
        with open(source_file, 'rb') as textfile:
            #get number of columns
            prevLine = ""
            table_found = False
            for line in textfile.readlines():
                #print line   
                line = line.rstrip()#remove newline characters
                if bool(re.search(starting_row, line)): #search for the starting row
                    table_found = True
                    new_table = Table()
                    new_table.addName(prevLine.split(demiliter)[0])
                    log.debug("maturity list {}".format(line))
                    new_table.addMaturityList(line.split(demiliter)) #add Annualised row 
                elif bool(re.search(testing, line)): #search if the line format is good   
                    #this is the data line
                    tempList = line.split(demiliter)
                    tempRating = tempList.pop(0)  #get the rating AAA, BB
                    new_table.addRating(tempRating)
                    new_table.addDataList(tempList) # add the data list, without the first item which is poped
                else:
                    #if table_found = True, it means we have reached the table bottom
                    if table_found: 
                        table_found = False 
                        tableList.append(new_table)
                prevLine = line
            if table_found: #if it is the end of file and still inside a table
                tableList.append(new_table)
        textfile.close
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.debug("{} {} {} {}".format(exc_type, fname, exc_tb.tb_lineno, e.message))
        raise e
        
    
    #if there is nothing int the file, just stop
    if not tableList:
        log.error("{}".format(ERROR_104))
        raise TransformationException(ERROR_104)
    #==============================================================================
    #write to the new file
    try:
        destination_file = output_folder + output_file    
        with open(destination_file, 'wb') as csv_out:
            #write the header    
            writer = csv.DictWriter(csv_out, fieldnames=header_row)
            writer.writeheader()
            #write the rest of data    
            mywriter = csv.writer(csv_out)        
            for table in tableList:
                if len(table.getName()) > 0: 
                    ratingList = table.getRatingList()
                    maturityList = table.getMaturityList()
                    dataList = table.getDataList()
                    log.debug("Rating list: {}".format(ratingList))
                    log.debug("Maturity list: {}".format(maturityList))
                    #print dataList
                    #print dataList[0][2]
                    #break
                    for i in range(len(ratingList)):
                        for j in range(len(maturityList)):
                            for k in bdcs_type:
                                dataNode = list(fixed_data)
                                dataNode.append(ratingList[i])
                                dataNode.append(maturityList[j])
                                dataNode.append(k)
                                dataNode.append(dataList[i][j])
                                dataNode.append(dataList[i][j])
                                dataNode.append(dataList[i][j])
                                #print dataNode
                                if (len(dataList[i][j]) > 0):
                                    mywriter.writerows([dataNode])
        csv_out.close
        log.info("Processing done {}".format(destination_file))
        #print "======================================"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.debug("{} {} {} {}".format(exc_type, fname, exc_tb.tb_lineno, e.message))
        raise e
        
#==============================================================================
if __name__ == "__main__":
    main(sys.argv[1:]) 