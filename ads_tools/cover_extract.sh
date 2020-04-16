#!/bin/bash

# Script that reads in a bunch of papers in pdf, extracts the first page, and create a pdf with 
# all the first pages. Papers need to be named "paper_x.pdf"

#File path
file_path="/home/roberto/UNAM/IRyA/pubs/"

# Better define by hand, in case some paper is unwanted
file_number=(0 1 2 3 4 7 8 9 10 11 14 17 19 20 21 22 23) 

echo "Extracting covers"

for element in ${file_number[*]}
do  
	printf " %s\n" "paper_"$element".pdf"
	pdftk $file_path"paper_"$element".pdf" cat 1 output $file_path"cover_"$element".pdf"
done

pdftk $file_path"cover*.pdf" cat output $file_path"rgm_covers_20182019.pdf"
