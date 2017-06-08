#!/bin/bash
cat $(dirname "$0")/logs/service.pid| nawk '{ system("kill -9 "$1);}'

