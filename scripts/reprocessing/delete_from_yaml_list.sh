#!/usr/bin/env bash

# create a test dataset

# Values used when moving data around
#    old_base='/g/data/xu18/ga/'
#    new_base='/g/data/u46/users/dsg547/test_data/c3/'

is_test=0 # True
#is_test=1 # False
if [ $is_test = 0 ] ; then
    old_base='/g/data/u46/users/dsg547/test_data/c3/'
else
    old_base='/g/data/xu18/ga/'
fi

ard_path="${1%/*}/"
old_path="$old_base$ard_path"
echo $old_path

rm -r $old_path

