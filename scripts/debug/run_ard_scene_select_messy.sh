#!/bin/bash

echo If module load breaks check on a clean environment
module use /g/data/v10/public/modules/modulefiles
module use /g/data/v10/private/modules/modulefiles

module load ard-scene-select-py3-dea/20210216
module load h5-compression-filters/20200612
module load dea

SSPATH=$PWD/../../

#PRODUCTS = '["ga_ls5t_level1_3", "ga_ls7e_level1_3", \
#         "usgs_ls5t_level1_1", "usgs_ls7e_level1_1", "usgs_ls8c_level1_1"]'

# You'll need a scratch directory
# mkdir scratch

# so it uses the dev scene select
# echo $PYTHONPATH
[[ ":$PYTHONPATH:" != *":$SSPATH:"* ]] && PYTHONPATH="$SSPATH:${PYTHONPATH}"
# echo $PYTHONPATH

#  local code local work dir, ls8
# 
time python3 ard_scene_select_messy.py --products '["usgs_ls8c_level1_1"]' --workdir scratch/  --pkgdir  scratch/ --logdir scratch/  --env $PWD/c3-samples-index-datacube.env --project u46 --walltime 10:00:00  --env /g/data/v10/projects/c3_ard/dea-ard-scene-select/scripts/prod/ard_env/prod-wagl.env #--run-ard  # --products '["usgs_ls8c_level1_1"]' --env /g/data/v10/projects/c3_ard/dea-ard-scene-select/scripts/prod/ard_env/prod-wagl.env
