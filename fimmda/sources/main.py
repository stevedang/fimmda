"""
Created on Wed Mar 01 10:10:57 2017
@author: @author: Murex Integration 2017
"""
import os, sys, shutil, subprocess, logging
from os import mkdir, listdir
from os.path import isfile, join
from datetime import datetime
import ConfigParser
from mapping.fimmdaException import *
from templates import tbill, zcyc, zeroSpread, cd, cp, parSpread, parYield

def main():
	logger = logging.getLogger(__name__)
	logging.basicConfig(format='%(asctime)s  - [%(levelname)s][%(name)s] - %(message)s')
	#sys.path.append("sources/mapping")
	#from exceptions.py import *

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
		tbill.main(input_file)
	#If the file name contains the format of ZERO Spread file name
	elif config.get("Files","zeroSpread_file") in input_file:
		zeroSpread.main(input_file)
	#If the file name contains the format of Par Spread file name
	elif config.get("Files","parSpread_file") in input_file:
		parSpread.main(input_file)
	#If the file name contains the format of Par Yield file name
	elif config.get("Files","parYield_file") in input_file:
		parYield.main(input_file)
	#If the file name contains the format of CP file name
	elif config.get("Files","cp_file") in input_file:
		cp.main(input_file)
	#If the file name contains the format of CD file name
	elif config.get("Files","cd_file") in input_file:
		cd.main(input_file)
	#If the file name contains the format of ZCYC file name
	elif config.get("Files","zcyc_file") in input_file:
		zcyc.main(input_file)
	#If the file has the wrong format, no output file is generated
	# error message is printed out
	else:
		print ERROR_101, input_file
		error =  ERROR_101 + input_file

	#execute the command and write to log file to fimmda.log in the new folder under archive folder
	with open(log_file, 'wb') as out:
		# print out error if the file format is wrong
		if error:
			out.write(error)
			sys.exit(1)
		#else:
		#else run the command to generate the output, print out all stdout, stdin and stderr to fimmda.log file
			#return_code = subprocess.call(cmd, shell=True,stdout=out, stdin=out, stderr=out)
			#print "do nothing here"
	#Close once it is done95
	out.close

	#once it is done
	logger.info("Archiving the input file " + input_file+ " and output file"+ output_file+ " to "+new_folder)
	#clear the input folder, copy the input file into archive folder
	if input_file:
		shutil.copy2(input_folder+input_file, new_folder)

	#copy the output file into the archive folder
	for f in listdir(output_folder):
		if isfile(join(output_folder, f)):
			logger.info( "Archiving the output file" + f + " to " +new_folder)
			shutil.copy2(output_folder+f, new_folder)
		
if __name__ == '__main__':
	main()

