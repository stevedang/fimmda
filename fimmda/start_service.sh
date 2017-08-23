#!/bin/bash
unset PYTHONPATH
unset PYTHONHOME

##############################
#check the os and assign the python commands
OS_TYPE=`uname`
if [ "$OS_TYPE" = "SunOS" ]; then
	python_command="python2.7" #if it is solaris
	awk_command="nawk" #if it is solaris
else
	python_command="python.exe" #if this is cygwin
	awk_command="awk" #if this is cygwin
fi
##############################
config_parser()
{
	local search_string=$2
	local properties_file=$1
	local __resultvar=$2	
	local myresult=$($awk_command -F "=" '/'$search_string'/ {sub(/^[ \t\r\n]+/, "", $2); sub(/[ \t\r\n]+$/, "", $2);print $2}' $properties_file)
	eval $__resultvar="'$myresult'"
}

##############################
#config file
CONFIGFILE="sources/properties.ini"

load_variables()
{
	#the current working folder 
	BASEDIR=$(dirname $0)
	
	#time each loop in seconds, by default it is 60 seconds
	config_parser $CONFIGFILE LOOPTIME 
	
	#input folder where we scan and pick up the file
	#input_folder="input"
	config_parser $CONFIGFILE input_folder
	#output folder where we retrieve the transformed file
	#output_folder="output"
	config_parser $CONFIGFILE output_folder

	#the source folder where the main.py resides
	#source_folder="./sources"
	config_parser $CONFIGFILE source_folder 

	# the log folder
	#LOGFOLDER="logs"
	config_parser $CONFIGFILE LOGFOLDER 

	#log file to write out all the information
	#LOGFILE="service.log"
	config_parser $CONFIGFILE LOGFILE

	#result file
	#RESULTFILE="output.log"
	config_parser $CONFIGFILE RESULTFILE

	#pid file to kill off the daemon 
	#PIDFILE="service.pid"
	config_parser $CONFIGFILE PIDFILE

	#filename
	filename=""

	#config file
	#CONFIGFILE="properties.ini"

	#MDIT folder and MDIT commands
	config_parser $CONFIGFILE mdit_folder
	config_parser $CONFIGFILE mdit_command
	#mdit_folder="../"
	#mdit_command="./marketdataInterface.sh -f "
	
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
	[ ! -f $BASEDIR/$CONFIGFILE ] && { echo "Config file does not exist. Exiting"; exit 1; }

	
}
#================================================
#Function write log
function writeToLog() {
	timeAndDate=$(date +"%Y-%m-%d %T,%3N")
	echo "$timeAndDate - $1"
}
#================================================
#Function check if any service is running
#kill all current processes
function killMe(){
    local me=`basename "$0"`
    cat $BASEDIR/$LOGFOLDER/$PIDFILE| $awk_command '{ system("kill -TERM -"$1);}' 2> /dev/null
    > $BASEDIR/$LOGFOLDER/$PIDFILE
    ps -ef| grep $me| grep -v $$| grep -v grep | $awk_command '{ system("kill -9 "$2);}' 2> /dev/null
}
#================================================
#Function run_mdit, to execute the MDIT file
#print out result whether it is OK or FAILED 
function run_mdit() {
	#Unsetting the IFS
	IFS=$SAVEIFS
	
	#run the command
	TEMPFILE=/tmp/transformation_log_$$.log
	echo $BASEDIR/$mdit_folder/$mdit_command $1 3>&1 2>&1 1>&3 | tee -a $TEMPFILE
	$BASEDIR/$mdit_folder/$mdit_command $1 3>&1 2>&1 1>&3 | tee -a $TEMPFILE
	
	LASTPID=$!

	while kill -0 $LASTPID 2>/dev/null; do
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
	TEMPFILE=/tmp/transformation_log_$$.log

	#return the result
	local __myresult=$2

	echo $python_command $BASEDIR/$source_folder/main.py $1 3>&1 2>&1 1>&3 | tee -a $TEMPFILE
	$python_command $BASEDIR/$source_folder/main.py $1 3>&1 2>&1 1>&3 | tee -a $TEMPFILE

	LASTPID=$!

	while kill -0 $LASTPID 2> /dev/null; do
		sleep 1
	done

	if grep "ERROR" $TEMPFILE > /dev/null 
	then
		writeToLog "[FAILED] $1 was unsuccesfull"| tee -a $BASEDIR/$LOGFOLDER/$RESULTFILE 
		__myresult="FAILED"
	else
		__myresult="OK"
	fi

	rm $TEMPFILE
	
	#resetting the IFS
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")
}
###############################################
#run_service
#loop through input folder and send the file to transformation module
#then pick up output file and send to MDIT
function run_service() {
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
		writeToLog "Searching input file in  $BASEDIR/$input_folder"
		for file in `find $BASEDIR/$input_folder -name '*.csv'`
		do
			#getting the file name only
			filename=`basename $file`
			
			#execute the command to transform the source csv to MDIT csv format
			writeToLog "Calling the transformation module for $filename"
			run_transform $filename $result
			
			#once the file is ready send it to mdit
			#remove the input file
			rm $file 

			#if transformation failed, skip the mdit
			if [ "$result" = "FAILED" ]; then
				writeToLog "Failed to transform $filename"
				continue
			fi

			#scan the output folder and move all the newly created file to MDIT
			writeToLog "Searching output file in  $BASEDIR/$output_folder"
			for file2 in `find $BASEDIR/$output_folder -name '*.csv'`
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
#main program

#load all variables
load_variables

#move to base dir folder in case this script is triggered remotely from another place
cd $BASEDIR

#kill other process if they are still running
killMe

case "$1" in
      --daemon)
			#write output, error and everythihng to log file
			echo $$ >> $BASEDIR/$LOGFOLDER/$PIDFILE
			exec 1>>	$BASEDIR/$LOGFOLDER/$LOGFILE
			exec 2>>	$BASEDIR/$LOGFOLDER/$LOGFILE
			writeToLog "Starting deamon mode in background "
			run_service & 
            ;;
      --normal)
            writeToLog "Starting test mode in foreground..click Ctrl-D to stop"
			#write output and everything to both file and console		
			echo $$ >> $BASEDIR/$LOGFOLDER/$PIDFILE
			run_service | tee $BASEDIR/$LOGFOLDER/$LOGFILE 
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
