#!/usr/bin/env python
"""
Title                                       :cd.py
Description                        :This module defines the transformation logic for CD
Author                                  :DANG Steve
Python_version                :2.7
-------------------------------
Change log:
Version                                Date                                      Who                                      Description
v1.0                                        20170822                             Steve                                    1st release
"""
##########################################
import csv, re, sys, logging, os
import ConfigParser
from utilities import utilities
from utilities.TransformationException import * 

#define the log
log = logging.getLogger(__name__)
#from  utilities import contains_header, contains_same_number_of_columns
config = ConfigParser.ConfigParser()
#==============================================================================
# Main configuration from properties.ini
config.read("sources/config/properties.ini")
demiliter= config.get("General","demiliter")
input_folder = config.get("General","input_folder")
output_folder = config.get("General","output_folder")
#==============================================================================
# Mapping
config.read("sources/mapping/mapping.ini")
input_file = ""
output_file = config.get("CD","output_file")
csv_header = config.get("CD","csv_header")
row_format_reg = config.get("CD","row_format_reg")
header_row = config.get("CD","header_row").split(",")
fixed_data = config.get("CD","fixed_data").split(",")
#==============================================================================
def main(args):
    input_file = args
    source_file = input_folder + input_file
    log.info("Reading CD input file {}".format(source_file))

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
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.debug("{} {} {} {}".format(exc_type, fname, exc_tb.tb_lineno, e.message))
        raise TransformationException(ERROR_103 + source_file)
    #if there is nothing int the file, just stop
    if not dataList:
        raise TransformationException(ERROR_104)
    #==============================================================================
    #write to the new file
    try:
        date_field = utilities.getDateFromFileName(input_file)
        destination_file = output_folder + output_file + "_"+ date_field + ".csv" 
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
        log.info("Processing done {}".format(destination_file))
    except TransformationException as e:
        raise e
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log.debug("{} {} {} {}".format(exc_type, fname, exc_tb.tb_lineno, e.message))
        raise TransformationException(ERROR_102 + destination_file)
#==============================================================================
if __name__ == "__main__":
    main(sys.argv[1:]) 