#!/bin/bash
##############################
if [ "$OS_TYPE" = "SunOS" ]; then
	awk_command="nawk" #if it is solaris
else
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
	
	#archive folder
	config_parser $CONFIGFILE archive_folder
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
###############################

#load all variables
load_variables
cd $BASEDIR

#in case of errors, output to /dev/null
exec 2>/dev/null
#kill the services
echo "Killing the service"
cat $BASEDIR/$LOGFOLDER/$PIDFILE| $awk_command '{ system("kill -TERM -"$1);}'
ps -ef| grep start_service| grep -v grep | $awk_command '{ system("kill -9 "$2);}'

# do housekeeping, zip the log file
echo "Housekeep the log file"
current_time=$(date +"%Y%m%d_%H%M%S")
zip $BASEDIR/$LOGFOLDER/service_$current_time.zip $(dirname "$0")/logs/*.log
> $BASEDIR/$LOGFOLDER/$LOGFILE
> $BASEDIR/$LOGFOLDER/$RESULTFILE


# do housekeeping, zip all the archive folder
echo "Zipping all the output files for housekeeping"
current_time=$(date +"%Y%m%d_%H%M%S")
find $BASEDIR/$archive_folder/* -type d -exec zip $BASEDIR/$archive_folder/archive_$current_time.zip {} +
find $BASEDIR/$archive_folder/* -type d -exec rm -rf {} +

#empty the service.pid
> $BASEDIR/$LOGFOLDER/$PIDFILE


