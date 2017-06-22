#!/usr/bin/env python
"""
Created on Wed Mar 01 10:10:57 2017
@author: @author: Murex Integration 2017
"""
#from  utilities import *
import csv, sys, re
import ConfigParser
from mapping.fimmdaException import * 
#from  utilities import contains_header, contains_same_number_of_columns
config = ConfigParser.ConfigParser()
config.read("sources/mapping/fimmda.mapping")
#==============================================================================
# Main constants
demiliter= config.get("General","demiliter")
input_folder = config.get("General","input_folder")
output_folder = config.get("General","output_folder")
input_file = ""
output_file = config.get("TBILL","output_file")
csv_header = config.get("TBILL","csv_header")
row_format_reg = config.get("TBILL","row_format_reg")
header_row = config.get("TBILL","header_row").split(",")
fixed_data = config.get("TBILL","fixed_data").split(",")
#==============================================================================
def main(args):
	input_file = args
	source_file = input_folder + input_file
	print "Reading TBill input file ",source_file
	dataList = []
	# open csv file
	try:
		with open(source_file, 'rb') as textfile:
			#get numbe of columns
			for line in textfile.readlines():
				#print line   
				line = line.rstrip()#remove newline characters
				if bool(re.search(row_format_reg, line)): #search if the line format is good            
					dataList.append(line.split(demiliter))
		textfile.close
	except:
		raise FimmdaException(ERROR_103+source_file)
		sys.exit()
	#if there is nothing int the file, just stop
	if not dataList:
		raise FimmdaException(ERROR_104)
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
			for list2 in dataList:
				dataNode = list(fixed_data)
				dataNode.append(list2[0]+"D")
				dataNode.append(list2[1])
				dataNode.append(list2[1])
				dataNode.append("");
				dataNode.append("");
				mywriter.writerows([dataNode])
		csv_out.close
		print "Processing done", destination_file
		print "======================================"
	except:
		raise FimmdaException(ERROR_102+destination_file)
#==============================================================================
if __name__ == "__main__":
	main(sys.argv[1:]) 