#!/usr/bin/env bash

# create a test dataset

# Values used when moving data around
#    old_base='/g/data/xu18/ga/'
#    new_base='/g/data/u46/users/dsg547/test_data/c3/reprocessing/ard_new'

#is_test=0 # True
is_test=1 # False
if [ $is_test = 0 ] ; then
    #old_base='/g/data/u46/users/dsg547/test_data/c3_reprocess/'
    old_base='/g/data/u46/users/dsg547/test_data/c3/reprocessing/ard_standard/'
else
    old_base='/g/data/xu18/ga/'
fi

ard_path="${1%/*}/"
old_path="$old_base$ard_path"
echo $old_path

rm -r $old_path

