"""
Title                                       :main.py
Description                        :This module defines the starting point for transformation module
Author                                  :DANG Steve
Python_version                :2.7
-------------------------------
Change log:
Version                                Date                                      Who                                      Description
v1.0                                        20170822                             Steve                                    1st release

"""
##########################################

import os, sys, shutil, subprocess, logging
from logging.handlers import RotatingFileHandler
from logging import handlers
from logging.config import fileConfig
from os import mkdir, listdir
from os.path import isfile, join
from datetime import datetime
import ConfigParser
from utilities.TransformationException import *
from templates import tbill, zcyc, zeroSpread, cd, cp, parSpread, parYield


#Read the config Parser from properties.ini and mapping.ini
config = ConfigParser.ConfigParser()
config2 = ConfigParser.ConfigParser()
config.read("sources/config/properties.ini")
config2.read("sources/mapping/mapping.ini")

#define the log at root level
#logging.basicConfig(format='%(asctime)s - [%(levelname)s][%(module)s] - %(message)s', stream=sys.stdout, mylevel)
fileConfig("sources/config/logging.ini")
log = logging.getLogger()

def main():
    #Read the config Parser from properties.ini and mapping.ini
    config = ConfigParser.ConfigParser()
    config2 = ConfigParser.ConfigParser()
    #If it is win32 (cygwin) use python.exe, otherwise use python2.7
    if "win32" == sys.platform:
        python_command="python.exe"
    else:
        python_command="python2.7"

    #Do sanity check for the arguments
    if len(sys.argv) < 2:
        print "Command Usage:", sys.argv[0], "[input_file]"
        sys.exit()
        
    #join the arguments in case there is a space in file name
    input_file = " ".join(sys.argv[1:])
    output_file = ""

    #create a new folder by the name and the pid of the current process
    config.read("sources/config/properties.ini")
    config2.read("sources/mapping/mapping.ini")
    input_folder = config.get("General","input_folder")
    archive_folder = config.get("General","archive_folder")
    output_folder = config.get("General","output_folder")

    #Get the pid and the timestamp to create the archive folder for every transformation
    #The format is YYYYMMDD-HHMMSS-TIMESTAMP-PID under archive folder
    pid = '{:d}'.format(os.getpid())
    now = datetime.now
    current_time = '{}'.format(now().strftime('%Y%m%d-%H%M%S-%f'))
    new_folder = archive_folder+current_time+"-"+pid

    #create the new folder
    mkdir(new_folder)

    #Command cmd to run the tbill
    #Error message is to store the error if being raise
    cmd = ""
    error = ""
    #If the file name contains the format of TBILL file name
    try:
        if config2.get("Files","tbill_file") in input_file:
            tbill.main(input_file)
        #If the file name contains the format of ZERO Spread file name
        elif config2.get("Files","zeroSpread_file") in input_file:
            zeroSpread.main(input_file)
        #If the file name contains the format of Par Spread file name
        elif config2.get("Files","parSpread_file") in input_file:
            parSpread.main(input_file)
        #If the file name contains the format of Par Yield file name
        elif config2.get("Files","parYield_file") in input_file:
            parYield.main(input_file)
        #If the file name contains the format of CP file name
        elif config2.get("Files","cp_file") in input_file:
            cp.main(input_file)
        #If the file name contains the format of CD file name
        elif config2.get("Files","cd_file") in input_file:
            cd.main(input_file)
        #If the file name contains the format of ZCYC file name
        elif config2.get("Files","zcyc_file") in input_file:
            zcyc.main(input_file)
        #If the file has the wrong format, no output file is generated
        # error message is printed out
        else:
            log.error("{} {}".format(ERROR_101, input_file))
            error =  ERROR_101 + input_file
    except IndexError as e:
        log.error("{}".format(e.message))
    except TransformationException as e:
        log.error("{}".format(e.message))
        sys.exit(0)

    #once it is done
    log.info("Archiving the input file to " + new_folder+ "/"+ input_file)
    #clear the input folder, copy the input file into archive folder
    if input_file:
        shutil.copy2(input_folder+input_file, new_folder)

    #copy the output file into the archive folder
    for f in listdir(output_folder):
        if isfile(join(output_folder, f)):
            log.info("Archiving the output file to " + new_folder+ "/"+ f)
            shutil.copy2(output_folder+f, new_folder)
        
if __name__ == '__main__':
    main()

