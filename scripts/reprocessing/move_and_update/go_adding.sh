#!/bin/bash

module use /g/data/v10/public/modules/modulefiles                               
module load parallel                                                            
module load dea/20200617                                                        

# indexing from ard
cat test_db_path.txt | parallel -j 8  -m -n 2 --line-buffer datacube  --config dsg547_dev.conf dataset add #--dry-run

