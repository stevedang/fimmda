#!/bin/bash
unset PYTHONPATH
unset PYTHONHOME

#check the os and assign the python commands
OS_TYPE=`uname`
if [ "$OS_TYPE" = "SunOS" ]; then
	python_command="python2.7" #if it is solaris
	awk_command="nawk" #if it is solaris
else
	python_command="python.exe" #if this is cygwin
	awk_command="awk" #if this is cygwin
fi

#the current working folder 
BASEDIR=$(dirname $0)

#time each loop in seconds, by default it is 60 seconds
LOOPTIME=2

#input folder where we scan and pick up the file
input_folder="input"

#output folder where we retrieve the transformed file
output_folder="output"

#the source folder where the main.py resides
source_folder="./sources"

# the log folder
LOGFOLDER="logs"

#log file to write out all the information
LOGFILE="service.log"

#result file
RESULTFILE="output.log"

#pid file to kill off the daemon 
PIDFILE="service.pid"

#filename
filename=""

#config file
CONFIGFILE="fimmda.properties"

#MDIT folder and MDIT commands
mdit_folder="../"
mdit_command="./marketdataInterface.sh -f "

######################################
#check and create input folder if no exist
[ ! -d $BASEDIR/$input_folder ] && { mkdir -p $BASEDIR/$input_folder; }

#check and create output folder if no exist
[ ! -d $BASEDIR/$output_folder ] && { mkdir -p $BASEDIR/$output_folder; }

#check if source folder exists
[ ! -d $BASEDIR/$source_folder ] && { echo "Cannot find source folder. Exiting.."; exit 1; } 

#check if log folder exists
[ ! -d "$BASEDIR/$LOGFOLDER" ] && { mkdir -p $BASEDIR/$LOGFOLDER; }

#check if config file exists
[ ! -f $BASEDIR/$source_folder/$CONFIGFILE ] && { echo "Config file does not exist. Exiting"; exit 1; }

#move to base dir folder in case this script is triggered remotely from another place
cd $BASEDIR

#================================================
#Function write log
function writeToLog() {
	timeAndDate=$(date +"%Y-%m-%d %T,%3N")
	echo "$timeAndDate - $1"
}

#================================================
#Function run_mdit, to execute the MDIT file
#print out result whether it is OK or FAILED 
function run_mdit() {
	#Unsetting the IFS
	IFS=$SAVEIFS
	
	#run the command
	TEMPFILE=/tmp/fimmda_log_$$.log
	$BASEDIR/$mdit_folder/$mdit_command $1 3>&1 2>&1 1>&3 | tee -a $TEMPFILE
	
	LASTPID=$!

	while kill -0 $LASTPID; do
		sleep 1
	done

	if grep "MDRS answer/log status: 'OK'" $TEMPFILE > /dev/null 
	then
		writeToLog "[OK] $filename was succesfull"| tee -a $BASEDIR/$LOGFOLDER/$RESULTFILE 
	else
		writeToLog "[FAILED] $filename was unsuccesfull"| tee -a $BASEDIR/$LOGFOLDER/$RESULTFILE 
	fi
	rm $TEMPFILE
			
	#resetting the IFS
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")
}
###########################################
#run_transform
#invoke transfrom module
#read output to print out to either OK or FAILED status
function run_transform() {
	#Unsetting the IFS
	IFS=$SAVEIFS
	
	#run the command
        output=$($python_command $BASEDIR/$source_folder/main.py $filename| 
	while IFS= read -r line
	do
		if [[  "$line" == *"[ERROR]"* ]]; then
			echo "KO"
			break
		fi
	done
	)

	if [ "KO" == "$output" ]; then
		writeToLog "[FAILED] $filename was unsuccesfull" | tee -a $BASEDIR/$LOGFOLDER/$RESULTFILE 
	fi
			
	#resetting the IFS
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")
}
###############################################
#run_fimmda
#loop through input folder and send the file to transformation module
#then pick up output file and send to MDIT
function run_fimmda() {
	#Set IFS setting is to prevent the space in the filename
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")

	#Loop through the input folder and run transformation
	#output file will be in output folder
	writeToLog "Start looping and transforming all the files"
	while true
	do
		#for file in `ls $BASEDIR/$input_folder/*.csv`
		#search for all csv files inside input folder
		writeToLog "Searching input file in  $BASEDIR/$input_folder/"
		for file in `find $BASEDIR/$input_folder/ -name '*.csv'`
		do
			#getting the file name only
			filename=`basename $file`
			
			#execute the command to transform the source csv to MDIT csv format
			writeToLog "calling the transformation module"
			#$python_command $BASEDIR/$source_folder/main.py $filename
			run_transform
			
			#once the file is ready send it to mdit
			#remove the input file
			rm $file 
			
			#scan the output folder and move all the newly created file to MDIT
			writeToLog "Searching output file in  $BASEDIR/$output_folder/"
			for file2 in `find $BASEDIR/$output_folder/ -name '*.csv'`
			do
				#move the transformed file to mdit input folder
				filename2=`basename $file2`
				writeToLog "Moving $filename2 to mdit folder $mdit_folder"
				mv $file2 $mdit_folder/input
				
				#execute the MDIT
				writeToLog "Executing MDIT"
				run_mdit $filename2
			done
		done

		#sleep until the next loop
		sleep $LOOPTIME
	done
	#turn IFS back
	IFS=$SAVEIFS
}
########################################################
#main programm
case "$1" in
      --daemon)
			#write output, error and everythihng to log file
			echo $$ >> $BASEDIR/$LOGFOLDER/$PIDFILE
			exec 1>>	$BASEDIR/$LOGFOLDER/$LOGFILE
			exec 2>>	$BASEDIR/$LOGFOLDER/$LOGFILE
			writeToLog "Starting deamon mode in background "
			run_fimmda & 
            ;;
      --normal)
            writeToLog "Starting test mode in foreground..click Ctrl-D to stop"
			#write output and everything to both file and console		
			echo $$ >> $BASEDIR/$LOGFOLDER/$PIDFILE
			run_fimmda | tee $BASEDIR/$LOGFOLDER/$LOGFILE 
            ;;
       --help)
            echo "Usage: $0 --[option]"
			echo "Options:"
            echo "    daemon:"
            echo "            Run in background. Process will still run when session is closed.  Need to run stop command to kill."
            echo "    normal:"
            echo "            Run in forground. Process will be killed when session is closed."
            echo "    help:"
            echo "            Print out the menu"
            exit 1
			;;				
          *)
            echo "Unknown command, run help for more option."
            echo "Usage: $0 --help"
            exit 1
            ;;
esac
