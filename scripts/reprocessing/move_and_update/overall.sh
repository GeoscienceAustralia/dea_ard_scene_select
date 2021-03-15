#!/bin/bash

# Pre-steps
#Setting up the test db
# ./delete_odc.sh  # remove the old DB
#./archive_test_db_index.sh ( this will run go_add.sh with ARD scenes too)

# Create the files of scene info
# ../go_log_2_r_ard_a.sh
# Main files produced;
# For step 2.2b -Archive the staged for deletion original dataset. 
#     uuid_file = "old_ards_to_archive.txt"
# For step1.1/1.2/1.4 - cp and update the scenes to be archived. 
#    old_ard_yaml_file = "old_ard_yaml.txt"
# input for the new ARD
#    l1_new_dataset_file = "l1_new_dataset_path.txt"

# The steps in step 1
# Step 1 – duplicate dataset to be archived in staging area
# 1.       Duplicate the [to be] archived dataset in “staging for removal” location”

#2.       Update location [in ODC] to point to
#         location in “staged for removal location”
# Note this is initially setup to just run on the test db
# edit ../step1.sh to change the base dirs

# ./go_step1.sh # steps 1.1 and 1.2
#3.       Wait prerequisite flush period (until queue empties) - 2 hours?
#4.       Trash original
# edit ../delete_from_yaml_list.sh to change the base dirs
#./go_delete.sh

# does ../parra_delete.sh then ../delete_from_yaml_list.sh
