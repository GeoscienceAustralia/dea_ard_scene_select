#!/bin/bash
module purge
module load pbs

DIR="$(cd "$(dirname "$0")" && pwd)"
echo $DIR

source $DIR/wagl.env

#is_test=0 # True
is_test=1 # False
if [ $is_test = 0 ] ; then
    
    level1_list=$DIR'/short_l1_new_dataset_path.txt'
    base_dir=$DIR/scratch
    pkgdir=$base_dir
    project='u46'
    index_datacube_env=$DIR'/dsg547_dev.env'
    archive_list=$DIR'/short_old_ards_to_archive.txt'
    #test=' --test '
    
else
    level1_list=$DIR'/l1_new_dataset_path.txt'
    archive_list=$DIR'/old_ards_to_archive.txt'
    base_dir='/g/data/v10/work/c3_ard'
    pkgdir='/g/data/xu18/ga'
    project='v10'
    index_datacube_env='/g/data/v10/projects/c3_ard/dea-ard-scene-select/scripts/prod/ard_env/index-datacube.env'
    test=' '
fi


ard_pbs --level1-list $level1_list --workdir $base_dir/workdir --pkgdir $pkgdir  --env $DIR'/wagl.env' --project $project --walltime 07:30:00 --index-datacube-env $index_datacube_env --logdir $base_dir/logdir --archive-list $archive_list $test
