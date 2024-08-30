#!/bin/bash

PROCESS="python3.11 /home/student/Desktop/logger/logger.py"
PID=$(sudo pidof "$PROCESS")

if [ -z "$PID" ]; then
	echo "Proces $PROCESS not found."
else
	sudo kill $PID
	echo "Done $PID"
fi

$PROCESS
