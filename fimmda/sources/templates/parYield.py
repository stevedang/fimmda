#!/usr/bin/env python
"""
Created on Wed Mar 01 10:10:57 2017
@author: Murex Integration 2017
"""
#==============================================================================
    
import csv, re, sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("sources/mapping/fimmda.mapping")
#==============================================================================
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
# Main constants
demiliter= config.get("General","demiliter")
input_folder = config.get("General","input_folder")
output_folder = config.get("General","output_folder")
input_file = ""
csv_header = config.get("PAR_YIELD","csv_header")
output_file = config.get("PAR_YIELD","output_file")
row_format_reg = config.get("PAR_YIELD","row_format_reg")
header_row = config.get("PAR_YIELD","header_row").split(",")
fixed_data = config.get("PAR_YIELD","fixed_data").split(",")
#==============================================================================
def main():
	#script, filename = argv
	source_file =  input_folder + input_file
	print "Reading Par Yield input file ",source_file

	dataList = []
	# open csv file
	try:
		with open(source_file, 'rb') as textfile:
			#get numbe of columns
			for line in textfile.readlines():
				#print line   
				line = line.rstrip()#remove newline characters
				if bool(re.search(row_format_reg, line)): #search if the line format is good            
					dataList.append(line.split(demiliter));
		textfile.close;
	except:
		print "Error when trying to open the file!" , source_file;
		sys.exit()
	#if there is nothing int the file, just stop
	if not dataList:
		print("There is nothing in the source file")
		sys.exit()
	#==============================================================================
	#write to the new file
	try:
		destination_file = output_folder + output_file    ;
		with open(destination_file, 'wb') as csv_out:
			#write the header    
			writer = csv.DictWriter(csv_out, fieldnames=header_row);
			writer.writeheader();     
			#write the rest of data    
			mywriter = csv.writer(csv_out)  ;      
			for list2 in dataList:
				dataNode = list(fixed_data);
				dataNode.append(_getMaturity(list2[0]));
				dataNode.append(list2[1]);
				dataNode.append(list2[1]);
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