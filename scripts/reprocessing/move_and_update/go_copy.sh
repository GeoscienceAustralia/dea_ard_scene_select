#!/bin/bash

module use /g/data/v10/public/modules/modulefiles                               
module load parallel                                                            
module load dea/20200617                                                        

# adding the base dir to the location info...
# awk '{print "/g/data/xu18/ga/" $0}' old_ard_yaml.txt > test_db_path.txt

# indexing from ard
cat  short_old_ard_yaml.txt| parallel -j 8 -n 1 --line-buffer ./copy.sh 

