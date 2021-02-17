#!/bin/bash

module use /g/data/v10/public/modules/modulefiles                               
module load parallel

DIR="$(cd "$(dirname "$0")" && pwd)"

# Run step1.sh with a file
cat $1 | parallel -j 8  -m -n 1 --line-buffer $DIR/step1.sh 
