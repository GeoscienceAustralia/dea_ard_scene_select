#!/bin/bash

# Script to add scenes to the test database
module use /g/data/v10/public/modules/modulefiles                               
module load parallel                                                            
module load dea/20200617                                                        

# adding the base dir to the location info...
#awk '{print "/g/data/u46/users/dsg547/test_data/c3/" $0}' short_old_ard_yaml.txt > short_test_db_path.txt

datacube  --config dsg547_dev.conf dataset search product='ga_ls8c_ard_3' | grep '^id: '

# indexing from ard
cat short_test_db_path.txt | parallel -j 8  -m -n 2 --line-buffer datacube  --config dsg547_dev.conf dataset add --confirm-ignore-lineage #--dry-run

datacube  --config dsg547_dev.conf dataset search product='ga_ls8c_ard_3' | grep '^id: '
