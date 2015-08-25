#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Usage: $0 [MATHEMATICAL EXPRESSION]"
	echo "Calculates given mathematical expression."
	exit
fi

result=$(echo "$1" | bc -l)

echo "$1 = $result"
