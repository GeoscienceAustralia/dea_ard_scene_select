#!/bin/bash

module use /g/data/v10/public/modules/modulefiles
module use /g/data/v10/private/modules/modulefiles
module load dea/20200617

./odc_connect.py --config dsg547_dev.conf --uuidfile old_ard_uuid.txt --stagingdir /g/data/u46/users/dsg547/test_data/c3_dump/ --ardbasedir /g/data/u46/users/dsg547/test_data/c3/
