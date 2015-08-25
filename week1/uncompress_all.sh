#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" || $# -eq 0 ]]; then
	# Print help
	echo "USAGE: $0 [dir]"
	echo "Uncompresses all gz-compressed files in given tree."
	exit
elif [ $# -ne 1 ]; then
	# Wrong number of arguments
	echo "Wrong number of arguments, see help with -h flag!"
	exit
elif [ ! -d $1 ]; then
	# Not a dir
	echo "$1 is not a directory!" 1>&2
	exit
fi

files=$(find $1 -name *.gz)

for file in $files; do
	gunzip $file
done
