#!/usr/bin/env bash
module use /g/data/v10/public/modules/modulefiles
module load dea

# Work on a dev DB
datacube --config dsg547_dev.conf system check
#exit 0

# This is for running local
datacube --config dsg547_dev.conf metadata add https://raw.githubusercontent.com/GeoscienceAustralia/digitalearthau/develop/digitalearthau/config/eo3/eo3_landsat_l1.odc-type.yaml

datacube --config dsg547_dev.conf product add https://raw.githubusercontent.com/GeoscienceAustralia/digitalearthau/develop/digitalearthau/config/eo3/products/l1_ls8.odc-product.yaml
datacube --config dsg547_dev.conf product add https://raw.githubusercontent.com/GeoscienceAustralia/digitalearthau/develop/digitalearthau/config/eo3/products/ard_ls8.odc-product.yaml

# Add the new l1 scenes.
# Based on short_l1_new_dataset_path.txt
datacube --config dsg547_dev.conf dataset add --confirm-ignore-lineage /g/data/u46/users/dsg547/test_data/c3/reprocessing/LC81010822019347/LC08_L1TP_101082_20191213_20201023_01_T1.odc-metadata.yaml
datacube --config dsg547_dev.conf dataset add --confirm-ignore-lineage /g/data/u46/users/dsg547/test_data/c3/reprocessing/LC81010802019347/LC08_L1TP_101080_20191213_20201023_01_T1.odc-metadata.yaml
datacube --config dsg547_dev.conf dataset add --confirm-ignore-lineage /g/data/u46/users/dsg547/test_data/c3/reprocessing/LC81010772019347/LC08_L1TP_101077_20191213_20201023_01_T1.odc-metadata.yaml

# Add the old ARD of the old L1 scene
# This part has a script
./go_adding.sh

# Archive the old L1 scene
#datacube --config dsg547_dev.conf dataset archive 760315b3-e147-5db2-bb7f-0e52efd4453d

#datacube --config dsg547_dev.conf dataset add --confirm-ignore-lineage 


echo product='ga_ls8c_ard_3'
datacube  --config dsg547_dev.conf dataset search product='ga_ls8c_ard_3' | grep '^id: '
echo product='usgs_ls8c_level1_1'
datacube  --config dsg547_dev.conf dataset search product='usgs_ls8c_level1_1' | grep '^id: '
# You now have a database with 0 level 1 ls8 scene
