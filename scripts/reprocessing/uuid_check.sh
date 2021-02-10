#!/bin/bash

module use /g/data/v10/public/modules/modulefiles    
module load parallel
module load dea


DIR="$(cd "$(dirname "$0")" && pwd)"

# Run step1.sh with a file
cat $1 | parallel -j 8  -m -n 1 --line-buffer datacube dataset info  | grep -e '^id: ' -e 'file:' -e 'status:'
