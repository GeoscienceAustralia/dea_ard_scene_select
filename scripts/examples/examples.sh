#!/bin/bash

module use /g/data/v10/public/modules/modulefiles
module use /g/data/v10/private/modules/modulefiles

module load ard-scene-select-py3-dea/20200909
module load h5-compression-filters/20200612
module load dea

SSPATH=$PWD/../../

# You'll need a scratch directory
# mkdir scratch

# so it uses the dev scene select
# echo $PYTHONPATH
[[ ":$PYTHONPATH:" != *":$SSPATH:"* ]] && PYTHONPATH="$SSPATH:${PYTHONPATH}"
# echo $PYTHONPATH

# production example
#python3 ard_scene_select.py --products '["ga_ls5t_level1_3"]' --workdir /g/data/v10/projects/landsat_c3/wagl_workdir  --pkgdir  /g/data/xu18/ga --logdir /g/data/v10/projects/landsat_c3/wagl_logdir --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project v10 --walltime 05:00:00 #--run-ard

#  local code local work dir, all products
# slow
#python3 ../../scene_select/ard_scene_select.py --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 05:00:00 #--run-ard

# This will use the dev ard scene select too..., all products
# unless the PYTHONPATH line above is commented out
# slow
time ard-scene-select  --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 02:30:00 --scene-limit 999999   --days-to-exclude '["2020-08-09:2020-09-03"]'

#  local code local work dir ls5t
# use ODC, fast for OEC
#time python3 ../../scene_select/ard_scene_select.py  --products '["ga_ls5t_level1_3"]' --days-to-exclude '["2020-08-09:2020-09-03"]' --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 05:00:00 #--stop-logging #--run-ard
#time python3 ../../scene_select/ard_scene_select.py  --products '["ga_ls5t_level1_3"]' --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 05:00:00 #--stop-logging #--run-ard

#  local code local work dir ls8c
# use ODC, fast for OEC#
#time python3 ../../scene_select/ard_scene_select.py  --products '["usgs_ls8c_level1_1"]'  --logdir scratch/ #--workdir scratch/  --pkgdir  scratch/ #--env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 05:00:00 #--stop-logging #--run-ard

#  local code local work dir # 
#python3 ../../scene_select/ard_scene_select.py  --products '["usgs_ls8c_level1_1"]' --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 05:00:00 #--run-ard

# local code local work dir and skipping odc
#python3 ../../scene_select/ard_scene_select.py --usgs-level1-files small_Landsat_Level1_Nci_Files.txt --workdir scratch/  --index-datacube-env c3-samples-index-datacube.env --pkgdir  scratch/ --logdir scratch/ --project u46 --walltime 05:00:00 #--run-ard  --env prod-wagl.env 

# prod module local work dir and skipping odc
#ard-scene-select --usgs-level1-files small_Landsat_Level1_Nci_Files.txt --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --project v10 --walltime 05:00:00 #--run-ard

# skipping odc
#python3 ard_scene_select.py  --usgs-level1-files small_Landsat_Level1_Nci_Files.txt

# using Australian_Wrs_list.txt
#python3 ../../scene_select/ard_scene_select.py  --usgs-level1-files ../../tests/test_data/All_Landsat_Level1_Nci_Files.txt  --workdir scratch/ --allowed-codes ../../tests/test_data/standard_wrs_list.txt  --logdir scratch/

#python3 ../../scene_select/ard_scene_select.py  --products '["2020-08-09:2020-08-30", "2020-09-02:2020-09-05"]' --workdir scratch/  --pkgdir  scratch/ --logdir scratch/ --env /g/data/v10/Landsat-Collection-3-ops/OFFICIAL/Collection-3_5.4.1.env --project u46 --walltime 05:00:00 #--stop-logging
