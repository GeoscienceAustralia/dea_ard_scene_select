#!/bin/bash

# Script to add scenes to the test database
module use /g/data/v10/public/modules/modulefiles                               
module load parallel                                                            
module load dea/20200617                                                        

echo product='ga_ls8c_ard_3'
datacube  --config dsg547_dev.conf dataset search product='ga_ls8c_ard_3' | grep -e '^id: ' -e 'file:'
