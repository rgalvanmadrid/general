#!/bin/bash

# Shell script that makes a backup of a list of folders in Draco to one of the massive storage spaces within the IRyA network
# This implementation skips over "non-regular files". If one wants to preserve symlinks, use: 
# To copy symlinks, use --links.
# To copy the files they are pointing to, use --copy-links.

######## DEFINED BY USER ############################
username="roberto" #username in IRyA network
connection="saturno" #IRyA server to use for connection, e.g., arambolas, saturno, posgrado04, your own
content_path="/lustre/roberto/W49_CMF/W49N_a_06_7M" #path of content in draco that will be synced off draco
backup_path="/fs/san11/roberto/copy_tests" #path for backup 
#NOTE that "backup_path" should end with "/" if "content_path" folder already exists in destination, 
#remove "/" at end of "backup_path" if "content_path" folder is created for the first time in destination. 
#Examples: "/fs/san11/username/backup_project", "/fs/nas03/other0/username/backup_project"
exclude="backup_exclude.txt" #file with list of paths to exclude from backup. NOTE that exclude paths are always relative to this script!
######################################################


if [[ $(hostname) == *"draco"* || $(hostname) == *"compute-0-11"* || $(hostname) == *"compute-0-12"* || $(hostname) == *"compute-0-13"* ||  $(hostname) == *"compute-0-14"* ]];
then
	echo "The master node draco is not for heavy processess, including copying large amounts of data."
	echo "Also, nodes compute-0-11 to compute-0-14 are reserved for the most memory-consuming processes."
	echo "Please connect to one of the computing nodes from compute-0-0 to compute-0-10 before running this script."
else
	echo ""You are using computing node "$(hostname)"
	echo "You will sync "$content_path" in Draco to "$backup_path" within IRyA network."
	read -p "Press enter to continue:"
	rsync -atvP --exclude-from $exclude $content_path $username"@"$connection":"$backup_path
	echo "Backup finished."	
fi


