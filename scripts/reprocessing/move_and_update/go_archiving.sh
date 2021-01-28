#!/bin/bash

module use /g/data/v10/public/modules/modulefiles
module use /g/data/v10/private/modules/modulefiles

module load dea

# indexing from ard
cat bad_l1_uuids_to_archive.txt | parallel -j 8  -m -n 2 --line-buffer datacube  --config dsg547_dev.conf dataset archive 

