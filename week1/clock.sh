#!/bin/bash

function ctrl_c {
	# SIGINT handler
	echo "Bye bye"
	exit
}

# Handle SIGINT
trap ctrl_c SIGINT

while true; do
	# Repeatedly print date on the same line
	echo -ne "\r$(date)"
	sleep 1
done
