#!/usr/bin/env bash
module use /g/data/v10/public/modules/modulefiles
module load dea

is_test=0 # True
#is_test=1 # False
if [ $is_test = 0 ] ; then
    old_base='/g/data/u46/users/dsg547/test_data/c3/'
    new_base='/g/data/u46/users/dsg547/test_data/c3_dump_more/' ;
else
    old_base='/g/data/u46/users/dsg547/test_data/c3/'
    new_base='/g/data/u46/users/dsg547/test_data/c3_not_prod_yet/' ;
fi

ard_path="${1%/*}/"
#echo $ard_path
old_path="$old_base$ard_path"
new_path="$new_base$ard_path"
echo $old_path
echo $new_path
mkdir -p $new_path

rsync -av $old_path $new_path

echo product='ga_ls8c_ard_3'
datacube  --config dsg547_dev.conf dataset search product='ga_ls8c_ard_3' | grep -E -- '^id: |file:'

# Update needs documentation...
newyaml="$new_base$1"
echo $newyaml
datacube --config dsg547_dev.conf dataset update $newyaml  --location-policy forget #  --dry-run

echo product='ga_ls8c_ard_3'
datacube  --config dsg547_dev.conf dataset search product='ga_ls8c_ard_3' | grep -e '^id: ' -e 'file:'
#datacube  --config dsg547_dev.conf dataset search product='usgs_ls8c_level1_1' | grep -E -- '^id: |file:'
# You now have a database with 1 level 1 ls8 scene
