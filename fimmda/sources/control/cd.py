#!/usr/bin/env python
"""
Created on Wed Mar 01 10:10:57 2017
@author: Murex Integration Singapore
"""
import csv, re, sys
import ConfigParser
#from  utilities import contains_header, contains_same_number_of_columns
config = ConfigParser.ConfigParser()
config.read("sources/mapping/fimmda.properties")
#==============================================================================
# Main constants
demiliter= config.get("General","demiliter")
input_folder = config.get("General","input_folder")
output_folder = config.get("General","output_folder")
input_file = ""
output_file = config.get("CD","output_file")
csv_header = config.get("CD","csv_header")
row_format_reg = config.get("CD","row_format_reg")
header_row = config.get("CD","header_row").split(",")
fixed_data = config.get("CD","fixed_data").split(",")
#==============================================================================
def main():
	#script, filename = argv
	source_file = input_folder + input_file
	print "Reading CD input file ",source_file

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
		print "Error when trying to open the file!" , source_file
		sys.exit()
	#if there is nothing int the file, just stop
	if not dataList:
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
		print "Error when trying to write into the file!" , destination_file
#==============================================================================
if __name__ == "__main__":
	input_file = " ".join(sys.argv[1:])
	main() 