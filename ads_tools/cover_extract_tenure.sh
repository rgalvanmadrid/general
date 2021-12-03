#!/bin/bash

# Script that reads in a bunch of papers in pdf, extracts the first page, and create a pdf with 
# all the first pages. 

# In file_path:
# rm -f cover*.pdf
# ls *.pdf > list_aug14_jul20.txt

#File path
file_path="/home/roberto/UNAM/IRyA/pubs/"
file_list="list_aug14_jul20.txt"

echo "Extracting covers:"

#Read filenames
while var= read -r line; do
	if [ -z "${line}" ]; then
		echo "Ignoring empty line"
	else
		case "$line" in \#*) continue ;; esac
		echo ${line}
		pdftk $file_path${line} cat 1 output $file_path"cover_"${line}
	fi
done < $file_path$file_list

# In file_path
#pdftk cover_*.pdf cat output covers_rgm_aug14_jul20.pdf
