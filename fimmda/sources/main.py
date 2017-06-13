"""
Created on Wed Mar 01 10:10:57 2017
@author: @author: Murex Integration 2017
"""
import os, sys, shutil, subprocess
from os import mkdir
from datetime import datetime
import ConfigParser

#Read the config Parser from fimmda.properties
config = ConfigParser.ConfigParser()
#config.read("sources/fimmda.properties")

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
config.read("sources/fimmda.properties")
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

#the log file under new folder
log_file = new_folder + "/fimmda.log"
#start checking the file and write to log file

#Command cmd to run the tbill
#Error message is to store the error if being raise
cmd = ""
error = ""
#If the file name contains the format of TBILL file name
if config.get("Files","tbill_file") in input_file:
	cmd = python_command+" ./sources/templates/tbill.py "+input_file
#If the file name contains the format of ZERO Spread file name
elif config.get("Files","zeroSpread_file") in input_file:
	cmd = python_command+" ./sources/templates/zeroSpread.py "+input_file
#If the file name contains the format of Par Spread file name
elif config.get("Files","parSpread_file") in input_file:
	cmd = python_command+" ./sources/templates/parSpread.py "+input_file
#If the file name contains the format of Par Yield file name
elif config.get("Files","parYield_file") in input_file:
	cmd = python_command+" ./sources/templates/parYield.py "+input_file
#If the file name contains the format of CP file name
elif config.get("Files","cp_file") in input_file:
	cmd = python_command+" ./sources/templates/cp.py "+input_file
#If the file name contains the format of CD file name
elif config.get("Files","cd_file") in input_file:
	cmd = python_command+" ./sources/templates/cd.py "+input_file
#If the file name contains the format of ZCYC file name
elif config.get("Files","zcyc_file") in input_file:
	cmd = python_command+" ./sources/templates/zcyc.py "+input_file
#If the file has the wrong format, no output file is generated
# error message is printed out
else:
	print "Cannot recognize the file", input_file
	error =  "Cannot recognize the file" + input_file

#execute the command and write to log file to fimmda.log in the new folder under archive folder
with open(log_file, 'wb') as out:
	# print out error if the file format is wrong
	if error:
		out.write(error)
	else:
	#else run the command to generate the output, print out all stdout, stdin and stderr to fimmda.log file
		return_code = subprocess.call(cmd, shell=True,stdout=out, stdin=out, stderr=out)
#Close once it is done
out.close

#once it is done
print "Archiving the input file ", input_file, " and output file", output_file, " to ",new_folder
#clear the input folder, copy the input file into archive folder
if input_file:
	shutil.copy2(input_folder+input_file, new_folder)
#copy the output file into the archive folder
if output_file:
	shutil.copy2(output_folder+"*.csv", new_folder)

