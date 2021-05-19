'''
Script to delete "junk" files, or large files that will not be used anytime soon even if they are not junk. 
'''

import glob
import os
import shutil

root_path = "/lustre/roberto/ALMA_IMF/lines/normalized"
delete_type = "*ms.split.cal"

files_to_delete = glob.glob("/".join([root_path,"science_goal*","group*","member*","calibrated",delete_type]))

print('Files to delete are: \n')
print(files_to_delete)
print('\n')


# Note: raw_input for Python 2.7, i.e., if script is run within CASA 5.X
# use input instead if running in Python 3.X or CASA 6.X 
if raw_input("Do You Want To Continue? [y/n]") == "y":
    # do something
    for file in files_to_delete:
        if os.path.exists(file):
            print("Deleting {}".format(file))
            shutil.rmtree(file)
        else:
            print("{} does not exist. Will continue ignoring this.".format(file))
