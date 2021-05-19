#!/bin/bash

# Shell script that makes backup of a computer within/to the IRyA network
# This implementation skips over "non-regular files". If one wants to preserve symlinks, use: 
# To copy symlinks, use --links.
# To copy the files they are pointing to, use --copy-links.

##########   DEFINED BY USER:   ###########

username="fulanito" #username in IRyA network
connection="" #IRyA computer to use for connection

content_path="/home/fulanito/" #path of content in local computer for which backup is desired
backup_path="/fs/nasXX/other0/fulanito/my_backup/" #path for backup. 
#NOTE that it should end with "/" if destination folder already exists, remove "/" at end if destination folder is created for the first time

exclude="backup_exclude.txt" #file with list of paths to exclude from backup. NOTE that exclude paths are always relative to this script!

###########################################
echo "Starting backup of "$content_path" to "$backup_path" within IRyA network."
sudo rsync -rtv --exclude-from $exclude $content_path $username"@"$connection":"$backup_path

echo "Backup finished"
