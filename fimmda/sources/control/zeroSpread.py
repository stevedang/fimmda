#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 10:10:57 2017
@author: @author: Murex Integration 2017
"""
#from  utilities import *
import csv, re, sys, os, argparse
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("sources/mapping/fimmda.properties")

def _is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True
    
def _getMaturity(str2):
    maturity = "";
    try:    
        temp = float(str2);
        if temp.is_integer():
            maturity = str(int(temp)) + "Y";
        else: 
            maturity = str(int(temp * 12)) + "M";
        return maturity;
    except:
        print "something wrong with the maturity conversion"
#==============================================================================
table_name_list = [
                   ["PSU & Fis", "PSU"],
                   ["NBFCs","NBFC"],
                   ["CORPORATES","CORP"],
                   ["PSL PTC spread","PSL"],
                   ["SG","SDL"],
                   ["UDAY/Discom","UDAY"],
                   ["AT1","AT1"]                   
                   ]
rating_label_list = config.get("ZERO_SPREAD","rating_label_list")
demiliter= config.get("General","demiliter")
input_folder = config.get("General","input_folder")
output_folder = config.get("General","output_folder")
csv_header = config.get("ZERO_SPREAD","csv_header")
output_file = config.get("ZERO_SPREAD","output_file")
input_file = ""
row_format_reg = config.get("ZERO_SPREAD","row_format_reg")
header_row = config.get("ZERO_SPREAD","header_row").split(",")
fixed_data = config.get("ZERO_SPREAD","fixed_data").split(",")
starting_row = config.get("ZERO_SPREAD","starting_row")
testing = config.get("ZERO_SPREAD","testing")
bdcs_type = config.get("ZERO_SPREAD","bdcs_type").split(",")
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
            if _is_number(i): self.maturityList.append(_getMaturity(i))
            
    def addRating(self,str2):
        found = False
        for i in rating_label_list: #cross check with the valid list
            if i == str2:
                #add AAA, AAA+, AAA- ,etc. into the list
                #append the name, such as PSU AAA
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

def main():
	#input_file = sys.argv[1]
	#script, filename = argv
	source_file = input_folder + input_file
	print "Reading Zero Spread input file ",source_file
	tableList = []
	# open csv file
	try:
		with open(source_file, 'rb') as textfile:
			#get numbe of columns
			prevLine = ""
			table_found = False
			for line in textfile.readlines():
				#print line   
				line = line.rstrip()#remove newline characters
				if bool(re.search(starting_row, line)): #search for the starting row
					table_found = True
					new_table = Table()
					new_table.addName(prevLine.split(demiliter)[0])
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
	except Exception, err:
		print ("Error: %s.\n" % str(err))
		sys.exit()
	#if there is nothing int the file, just stop
	if not tableList:
		print("There is nothing in the source file")
		sys.exit()
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
								if (len(dataList[i][j]) > 0):
									mywriter.writerows([dataNode])
		csv_out.close
		print "Processing done", destination_file
		print "======================================"
	except Exception, err:
		print ("Error: %s.\n" % str(err))
#==============================================================================
if __name__ == "__main__":
	input_file = " ".join(sys.argv[1:])
	main()