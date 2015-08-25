#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Usage: $0 [MATHEMATICAL EXPRESSION]"
	exit
fi

RES=$(echo "$1" | bc -l)

echo "$1 = $RES"
