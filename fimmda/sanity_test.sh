#!/bin/bash
unset PYTHONPATH
unset PYTHONHOME

#check the os and assign the python commands
OS_TYPE=`uname`
if [ "$OS_TYPE" = "SunOS" ]; then
	python_command="python2.7" #if it is solaris
else
	python_command="python.exe" #if this is cygwin
fi

#the current working folder 
BASEDIR=$(dirname $0)

#time each loop in seconds, by default it is 60 seconds
LOOPTIME=60

#log file to write out all the information
LOGFILE="logs/service.log"

#input folder where we scan and pick up the file
input_folder="input"

#output folder where we retrieve the transformed file
output_folder="output"

#the source folder where the main.py resides
source_folder="./sources"

#MDIT folder and MDIT commands
mdit_folder="../"
mdit_command="./marketdataInterface.sh -f "

#move to base dir folder in case this script is triggered remotely from another place
cd $BASEDIR

#Redirect stdout ( > ) into a named pipe ( >() ) running "tee"
exec > >(tee -i $BASEDIR/$LOGFILE)
exec 2>&1

#Get its own PID and write pid to the log file
pid=$$
echo $pid > $BASEDIR/$PIDFILE
echo $!  >> $BASEDIR/$PIDFILE
#================================================
#Function write log
function writeToLog() {
	echo $1 >&2 
}
#================================================
#Function run_mdit, to execute the MDIT file
function run_mdit() {
	#Unsetting the IFS
	IFS=$SAVEIFS
	
	#run the command
	$BASEDIR/$mdit_folder/$mdit_command $1
	
	#resetting the IFS
	SAVEIFS=$IFS
	IFS=$(echo -en "\n\b")
}

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
		for file in `find $BASEDIR/$input_folder/ -name '*.csv'`
		do
			#getting the file name only
			filename=`basename $file`
			
			#execute the command to transform the source csv to MDIT csv format
			$python_command $BASEDIR/$source_folder/main.py $filename 
			
			#once the file is ready send it to mdit
			#remove the input file
			rm $file 
			
			#scan the output folder and move all the newly created file to MDIT
			for file2 in `ls $BASEDIR/$output_folder/*.csv`
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

run_fimmda  


