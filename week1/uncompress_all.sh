#!/bin/bash
if [ $# -ne 1 ]; then
	echo "USAGE: $0 [dir path]"
	exit
fi

if [ ! -d $1 ]; then
	echo "$1 is not a directory!" 1>&2
	exit
fi

files=$(find $1 -name *.gz)

for file in $files; do
	gunzip $file
done
