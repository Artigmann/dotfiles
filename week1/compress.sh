#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" || $# -eq 0 ]]; then
	# Help message
	echo "USAGE: $0 [dir] [filesize (kB)]"
	echo "Compresses all files over given filesize in given tree"
	exit
elif [ $# -ne 2 ]; then
	# Wrong number of arguments
	echo "Wrong number of arguments, see help with -h flag!" 1>&2
	exit
elif [ ! -d $1 ]; then
	# Not a dir
	echo "$1 is not a directory!" 1>&2
	exit
fi

find $1 -size +${2}k -exec gzip {} \;
