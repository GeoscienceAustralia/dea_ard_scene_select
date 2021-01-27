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

# The old L1 scene.
# 760315b3-e147-5db2-bb7f-0e52efd4453d
#datacube --config dsg547_dev.conf dataset add --confirm-ignore-lineage /g/data/u46/users/dsg547/test_data/c3/LC81150802019349/LC08_L1TP_115080_20191215_20191226_01_T1.tar

# Add the ARD of the old L1 scene
# id: fa083e38-a753-4a30-82f7-9deb27ee1602
# lineage:  level1:  - 760315b3-e147-5db2-bb7f-0e52efd4453d
#datacube --config dsg547_dev.conf dataset add /g/data/u46/users/dsg547/test_data/c3/ga_ls8c_ard_3/115/080/2019/12/15/ga_ls8c_ard_3-1-0_115080_2019-12-15_final.odc-metadata.yaml

# Archive the old L1 scene
#datacube --config dsg547_dev.conf dataset archive 760315b3-e147-5db2-bb7f-0e52efd4453d

#datacube --config dsg547_dev.conf dataset add --confirm-ignore-lineage 


echo product='usgs_ls8c_level1_1'
datacube  --config dsg547_dev.conf dataset search product='usgs_ls8c_level1_1' | grep '^id: '
# You now have a database with 0 level 1 ls8 scene
