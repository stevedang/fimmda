#!/bin/bash

BASEDIR=$(dirname "$0")
#kill the services
cat $BASEDIR/logs/service.pid| nawk '{ system("kill -TERM -"$1);}'

# do housekeeping, zip the log file
echo "Housekeep the log file"
current_time=$(date +"%Y%m%d_%H%M%S")
zip $BASEDIR/logs/service_$current_time.zip $(dirname "$0")/logs/service.log
> $BASEDIR/logs/service.log


# do housekeeping, zip all the archive folder
echo "Zipping all the output files for housekeeping"
current_time=$(date +"%Y%m%d_%H%M%S")
find $BASEDIR/archive/* -type d -exec zip $BASEDIR/archive/archive_$current_time.zip {} +
find $BASEDIR/archive/* -type d -exec rm -rf {} +

#empty the service.pid
> $BASEDIR/logs/service.pid 





