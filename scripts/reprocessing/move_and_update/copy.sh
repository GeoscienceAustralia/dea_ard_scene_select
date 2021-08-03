#!/usr/bin/env bash
module use /g/data/v10/public/modules/modulefiles
module load dea

# create a test dataset

# Values used when moving data around
#    old_base='/g/data/xu18/ga/'
#    new_base='/g/data/u46/users/dsg547/test_data/c3/'

is_test=0 # True
#is_test=1 # False
if [ $is_test = 0 ] ; then
    old_base='/g/data/u46/users/dsg547/test_data/c3/'
    new_base='/g/data/u46/users/dsg547/test_data/c3_dump_staging/' ;
else
    old_base='/g/data/xu18/ga/'
    old_base='/g/data/xu18/ga_staging/' ;
fi

ard_path="${1%/*}/"
#echo $ard_path
old_path="$old_base$ard_path"
new_path="$new_base$ard_path"
echo $old_path
echo $new_path
mkdir -p $new_path

rsync -av $old_path $new_path
