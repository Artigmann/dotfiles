#!/bin/bash
if [ $# -ne 2 ]; then
	echo "USAGE: $0 [dir path] [filesize (kB)]"
	exit
fi

if [ ! -d $1 ]; then
	echo "$1 is not a directory!" 1>&2
	exit
fi

files=$(find $1 -size +${2}k)

for file in $files; do
	gzip $file
done
