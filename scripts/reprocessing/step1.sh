#!/usr/bin/env bash
module use /g/data/v10/public/modules/modulefiles
module load dea

#is_test=0 # True # test
is_test=1 # False # production
if [ $is_test = 0 ] ; then
    old_base='/g/data/u46/users/dsg547/test_data/c3/reprocessing/ard_standard/'
    new_base='/g/data/u46/users/dsg547/test_data/c3/reprocessing/ard_new/'

    # setting up the testing env
    #old_base='/g/data/u46/users/dsg547/test_data/c3/reprocessing/ard_raw/'
    #new_base='/g/data/u46/users/dsg547/test_data/c3/reprocessing/ard_standard/'
else
    old_base='/g/data/xu18/ga/'
    new_base='/g/data/xu18/ga/reprocessing_staged_for_removal/'
fi

ard_path="${1%/*}/"
#echo $ard_path
old_path="$old_base$ard_path"
new_path="$new_base$ard_path"
echo $old_path
echo $new_path
mkdir -p $new_path

a_cmd="rsync"
#a_cmd="update"
if [ $a_cmd = "rsync" ] ; then
    rsync -av $old_path $new_path
else
    newyaml="$new_base$1"
    echo $newyaml
    datacube --config dsg547_dev.conf dataset update $newyaml  --location-policy forget #  --dry-run
fi
